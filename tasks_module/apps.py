"""tasks_module configuration"""

import atexit
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig


logger = logging.getLogger('gunicorn.error')

class TasksModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_module'

    def ready(self):
        """Override the ready method to start the scheduler."""
        from .helpers import update_task_similarities
        scheduler = BackgroundScheduler()
        # Run every minute, to ensure it executes during testing:
        scheduler.add_job(
            func=update_task_similarities,
            trigger="interval", seconds=60,
        )
        scheduler.start()
        # Shut down the scheduler when Django stops:
        atexit.register(teardown, scheduler)

def teardown(scheduler: BackgroundScheduler):
    """Shut down the scheduler.
    Args:
        scheduler (BackgroundScheduler): The scheduler to shut down.
    """
    logger.info("Shutting down the scheduler...")
    scheduler.shutdown()
