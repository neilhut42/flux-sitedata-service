import os
import logging
import time

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test

from celery import Celery

logger = logging.getLogger(__name__)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

celery_config = {
    'main': 'django_app',
    'namespace': 'CELERY',
}
if hasattr(settings, 'BROKER_URL') and settings.BROKER_URL:
    celery_config['broker'] = settings.BROKER_URL

app = Celery(**celery_config)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    time.sleep(5)
    logger.info('DEBUG_TASK SUCCESS!: {0!r}'.format(self.request))


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["GET"])
def debug_celery_view(request):
    debug_task.delay()
    return HttpResponse("OK!")
