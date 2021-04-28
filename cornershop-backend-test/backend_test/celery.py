import os

from celery import Celery

from .envtools import getenv
from celery.schedules import crontab



class CelerySettings:
    # Settings for version 4.3.0
    # see: https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html
    # important note: config var names do not match perfectly with celery doc, keep that in mind.
    # General settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#general-settings
    CELERY_ACCEPT_CONTENT = ["json"]
    # Time and date settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#time-and-date-settings
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = "UTC"
    # Task settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#task-settings
    CELERY_TASK_SERIALIZER = "json"
    # Task execution settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#task-execution-settings
    CELERY_ALWAYS_EAGER = getenv("CELERY_ALWAYS_EAGER", default="False", coalesce=bool)
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = getenv(
        "CELERY_EAGER_PROPAGATES_EXCEPTIONS", default="False", coalesce=bool
    )
    CELERY_IGNORE_RESULT = getenv("CELERY_IGNORE_RESULT", default="True", coalesce=bool)
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    CELERYD_TASK_TIME_LIMIT = 60 * 2  # hard time limit
    CELERYD_TASK_SOFT_TIME_LIMIT = int(CELERYD_TASK_TIME_LIMIT * 0.85)
    CELERY_ACKS_LATE = True
    CELERY_TASK_REJECT_ON_WORKER_LOST = True
    # Task result backend settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#task-result-backend-settings
    #redis://localhost:6379"
    CELERY_RESULT_BACKEND = getenv(
        "CELERY_RESULT_BACKEND_URL", default="redis://localhost:6379/3"
    )
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    # Message Routing
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#message-routing
    # BROKER_TASK_QUEUE_HA_POLICY = []
    CELERY_DEFAULT_QUEUE = "celery"
    CELERY_DEFAULT_EXCHANGE = CELERY_DEFAULT_QUEUE
    CELERY_DEFAULT_ROUTING_KEY = CELERY_DEFAULT_QUEUE
    # Message Routing
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#broker-url
    BROKER_URL = getenv("CELERY_BROKER_URL", default="redis://localhost:6379/2") #"redis://localhost:6379"
    BROKER_POOL_LIMIT = 10  # default is 10
    BROKER_CONNECTION_MAX_RETRIES = 0  # default is 100, ask joe why 0
    BROKER_HEARTBEAT = None
    # Worker
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#worker
    CELERYD_WORKER_LOST_WAIT = 20
    # Logging
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#logging
    CELERYD_HIJACK_ROOT_LOGGER = getenv(
        "CELERYD_HIJACK_ROOT_LOGGER", default="False", coalesce=bool
    )
    # Custom Component Classes (advanced)
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#custom-component-classes-advanced
    CELERYD_POOL_RESTARTS = True
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
    CELERY_BEAT_SCHEDULE = {
        "sample_task": {
            "task": "bonapetit.tasks.sample_task",
            "schedule": "10.0"#crontab(minute="*/1"),
        },
    }


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_test.settings")

settings = CelerySettings()

app = Celery("backend_test")
app.config_from_object(settings)
app.autodiscover_tasks()

"""
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    #sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    #sender.add_periodic_task(
     #   crontab(hour=7, minute=30, day_of_week=1),
      #  test.s('Happy Mondays!'),
    #)

@app.task
def test(arg):
    print(arg)"""