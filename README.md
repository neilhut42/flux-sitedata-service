# Hut Forty Two Django Application

Application boilerplate for Hut Forty Two Django webapps / microservices.

## Next Steps

- Read this.
- Replace the `$PROJECT_NAME` and `$PROJECT_DESCRIPTION` variables in `README.rst`. 
- Update the `CHANGELOG.rst`.
- Delete the `CHANGELOG_PROJECT.rst`.
- Copy .env.example to .env (keep .env.exampke as is, to help out the next developer who clones)
- Change `db_name_here` in `.env` and `.env.docker` to a unique name (the app name is a good one to use) to avoid clashing db names on shared docker volumes. 
- Delete this file (`README.md`)

## Features

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Latest Python 3.8 Heroku runtime environment.
- Out of the box Celery setup for remote and local development.
- Docker setup for easy and consistent local development.
- Sensible default configuration and useful tools.

## How to Use

Simply create a new repository in GitHub using this template and clone it down to your local machine.  Do the env stuff, get Docker running and boom.

## Env files

The app template includes settings for local development with Docker (see below).  These are in `.env.docker` and can mostly (bar the db name) be left alone.  This file is committed to source control and as such **SHOULD NOT CONTAIN ANY SECRETS**. For django env settings, copy `env.example` to `.env` and keep it out of source control. By default, the `.gitignore` in this project template does just that.

## Important note about Gemfury packages

Gemfury is where we host our private python packages.

Make sure you have set the `FURY_AUTH` token in your local environment variables or Heroku config variables for remote. 
The actual token value can be found in Keeper. You can set this in your `.bashrc` or `.bash_profile` file.  

Windows users can add this in Settings >  Related Settings > Advanced > Environment Variables.  

This must be done as a matter of course, otherwise the Docker or any other build will fail.

## Running locally with Docker

This includes a docker configuration that will run all the requisite components that will match a remote setup (i.e. Heroku) as closely as possible.  

These include:

- Gunicorn to serve the web files
- Nginx as a reverse proxy in front of the Gunicorn server
- Redis for caching / task broker
- Celery for deferred task operations
- Flower for local task monitoring (not available in Heroku 😢)

To get this up and running make sure you have Docker and Docker Compose set up on your machine.  On Windows and macOS, you can use [Docker Desktop](https://www.docker.com/products/docker-desktop).  For Linux, this will vary by distro:

- Install [Docker engine](https://docs.docker.com/engine/install/#server)
- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Then [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>)

Then it should just be a case of:

    docker-compose up

The first build will take a long time as the images are downloaded and built, but after that it should be fairly quick to bring the containers up and down.

You will need to create a superuser when first running the project, but this can be done by:

    docker-compose exec web python manage.py createsuperuser

and follow the prompts.  Any other django management commands (including custom ones) can be executed in a similar way.

## Install packages in a local venv

This may seem pointless with a Docker build, but it's easier for the Pycharm linter to work with a local venv than trying to get it to play nice with the docker ones. Settings > Project > Python Interpreter to set it up, then the usual:

    pip install -r requirements_docs.txt

In an activated venv shell.  Easiest way of doing this is to open a new terminal window in Pycharm after the creation of the venv.  You should see a shell prompt like `(venv_name) $` (or whatever your shell prompt is set up like) to indicate this.   


## How is this different to Django project templates?

Django templates (with `startapp`) are templated and are run locally.  Creating a project from a GitHub template
will give a "ready to run" project without the project name parsing etc. Using https://github.com/Hut42/heroku-django-template is now deprecated.

## But my project is now called "django_app" instead of a more semantic name? 

No. It really doesn't make a difference.  It's better to have all the core bits of the app on the same paths -
`django_app.settings`, `django_app.wsgi` etc. so we can do some really cool things in the future with monitoring and 
automation. 

## What is "bin" for?

It forms part of a necessary build step for Heroku to include any private requirements.  When Heroku updates its pip
version this will be removed.

## Does this work on Elastic Beanstalk / AWS deploys.

The application does, yes. To add the build config/steps, please see *unnamed_project*. 

## Does this include Celery?

Yes. The included Procfile / django_app.celery sets it all up. By default, the Heroku worker will be disabled. To actually use Celery tasks, enable this worker in the resources tab.  Redis must also be set up as well.  For local development you should be using Docker so this (should) all be working.  You can use Flower (https://flower.readthedocs.io/en/latest/) to monitor your tasks at http://localhost:8888.  To bump a test celery task onto the queue, go to http://localhost/celery - this will add a simple 5-second sleep type task onto the queue.  It should execute immediately in the browser but continue to finish on the queue.  Use Flower to confirm.  

## Celery is driving me crazy

This is probably because you have made code changes to your tasks, and not reloaded the service.  Celery removed the ability to have the worker live reloading on code changes. So when testing celery tasks locally make sure you have restarted the service:

    docker-compose restart celery

## Configuration

| Value                        | Default                        | .env Default                                    | Description                                                                                                                                                        |
|------------------------------|--------------------------------|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEBUG                        | `False`                        | `True`                                          | DEBUG mode for django. Should not be True when on any remote instance.  This includes dev/test!                                                                    |
| SECRET_KEY                   | `None`                         | `'django-isecure'`                              | Django SECRET_KEY. Must be set in Heroku env vars, otherwise build will fail.                                                                                      |
| DATABASE_URL                 | `None`                         | `None`                                          | Database connection string in URL type format.                                                                                                                     |
| DISABLE_DATABASE_SSL_REQUIRE | `False`                        | `not DEBUG`                                     | Disables the strict SSL requirement for Postgres connections. Must NOT be set to True in production.  You may need to set this to True in a local dev ENVIRONMENT. |
| SITE_ID                      | `1`                            | `1`                                             | Necessary for app to work as the contrib.sites framework is enabled. For single site apps, this can safely be left as the default.                                 |
| ADMIN_PATH                   | `None`                         | `'adm'`                                         | Path to Django admin. Make this something obscure.                                                                                                                 |
| EMAIL_USE_TLS                | `None`                         | `None`                                          | Email sending setting.                                                                                                                                             |
| EMAIL_HOST                   | `None`                         | `None`                                          | Email sending setting.                                                                                                                                             |
| EMAIL_HOST_PASSWORD          | `None`                         | `None`                                          | Email sending setting.                                                                                                                                             |
| EMAIL_HOST_USER              | `None`                         | `None`                                          | Email sending setting.                                                                                                                                             |
| EMAIL_PORT                   | `None`                         | `None`                                          | Email sending setting.                                                                                                                                             |
| DEFAULT_FROM_EMAIL           | `None`                         | `None`                                          | Email sending setting.                                                                                                                                             |
| ENVIRONMENT                  | `None`                         | `'local'`                                       | ENVIRONMENT description for internal purposes. Should be one of 'dev', 'test' 'live' on deployed instances.                                                        |
| SENTRY_ENVIRONMENT           | `ENVIRONMENT`                  | `ENVIRONMENT`                                   | ENVIRONMENT description for Sentry logging. Should be one of 'dev', 'test' 'live' on deployed instances.                                                           |
| SENTRY_DSN                   | `None`                         | `None`                                          | Endpoint for Sentry logging. Must be set for all remote instances.                                                                                                 |
| REDIS_URL                    | `None`                         | `None`                                          | Endpoint for redis instance.  Must be set when using Celery and not overriding BROKER_URL                                                                          |
| BROKER_URL                   | `REDIS_URL`                    | `REDIS_URL`                                     | Endpoint for redis instance.  Must be set when using Celery and not overriding BROKER_URL                                                                          |
| CELERY_TASK_ALWAYS_EAGER     | `False`                        | `True`                                          | Flags is Celery will execute tasks synchronously or asynchronously. See above Celery section for details.                                                          |
| CACHE_BACKEND                | `None`                         | `'django.core.cache.backends.dummy.DummyCache'` | Cache backend Django will use. See https://docs.djangoproject.com/en/3.2/topics/cache/.                                                                            |
| CACHE_LOCATION               | `None`                         | `None`                                          | Cache location. See https://docs.djangoproject.com/en/3.2/topics/cache/.                                                                                           |
| CACHE_USERNAME               | `None`                         | `None`                                          | Cache username. See https://docs.djangoproject.com/en/3.2/topics/cache/.                                                                                           |
| CACHE_PASSWORD               | `None`                         | `None`                                          | Cache password. See https://docs.djangoproject.com/en/3.2/topics/cache/.                                                                                           |
| ADMIN_SITE_HEADER            | `'Application administration'` | `None`                                          | Header in Django admin.                                                                                                                                            |
| ADMIN_SITE_TITLE             | `'Application site admin'`     | `None`                                          | Title in Django admin.                                                                                                                                             |
| ADMIN_INDEX_TITLE            | `'Application administration'` | `None`                                          | Index title in Django admin.                                                                                                                                       |
| GOOGLE_TAG_ID                | `None`                         | `None`                                          | Google Analytics / Tag manager id. MUST be set for live flux projects.                                                                                             |

## Deployment

Use the `deploy to Heroku` button in the README.rst once you have changed the name variables.

## Documentation

To build the documentation, install the documentation requirements from `requirements_docs.txt`:

    pip install -r requirements_docs.txt

Then use Sphinx to build the docs:

    make -C docs html

Compiled docs can be found in the `docs/_build` directory.
