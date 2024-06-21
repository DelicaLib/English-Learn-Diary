from celery.schedules import crontab

from backend.config import CeleryLogClearConfig

broker_url = 'redis://localhost:6379/2'
result_backend = 'redis://localhost:6379/3'

beat_schedule = {
    'clear_old_logs': {
        'task': 'ClearOldLogTask',
        'schedule': crontab(minute=CeleryLogClearConfig.CLEAR_LOGS_MINUTE, hour=CeleryLogClearConfig.CLEAR_LOGS_HOUR,
                            day_of_week=CeleryLogClearConfig.CLEAR_LOGS_DAY_OF_WEEK, day_of_month=CeleryLogClearConfig.CLEAR_LOGS_DAY_OF_MONTH,
                            month_of_year=CeleryLogClearConfig.CLEAR_LOGS_MONTH_OF_YEAR),
    },
}
