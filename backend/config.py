import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG') == "true"


class ClickHouseConfig:
    CLICKHOUSE_DB_NAME = os.getenv('CLICKHOUSE_DB_NAME')
    CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST')
    CLICKHOUSE_PORT = int(os.getenv('CLICKHOUSE_PORT'))
    CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER')
    CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')


class CeleryLogClearConfig:
    CLEAR_LOGS_MINUTE = os.getenv('CLEAR_LOGS_MINUTE')
    CLEAR_LOGS_HOUR = os.getenv('CLEAR_LOGS_HOUR')
    CLEAR_LOGS_DAY_OF_WEEK = os.getenv('CLEAR_LOGS_DAY_OF_WEEK')
    CLEAR_LOGS_DAY_OF_MONTH = os.getenv('CLEAR_LOGS_DAY_OF_MONTH')
    CLEAR_LOGS_MONTH_OF_YEAR = os.getenv('CLEAR_LOGS_MONTH_OF_YEAR')

    CLEAR_LOGS_MINUTE_INTERVAL = os.getenv('CLEAR_LOGS_MINUTE_INTERVAL')
    CLEAR_LOGS_HOUR_INTERVAL = os.getenv('CLEAR_LOGS_HOUR_INTERVAL')
    CLEAR_LOGS_DAY_INTERVAL = os.getenv('CLEAR_LOGS_DAY_INTERVAL')
    CLEAR_LOGS_MONTH_INTERVAL = os.getenv('CLEAR_LOGS_MONTH_INTERVAL')
    CLEAR_LOGS_YEAR_INTERVAL = os.getenv('CLEAR_LOGS_YEAR_INTERVAL')

    @classmethod
    def validate(cls):
        if not cls.CLEAR_LOGS_MINUTE:
            cls.CLEAR_LOGS_MINUTE = "*"
        if not cls.CLEAR_LOGS_HOUR:
            cls.CLEAR_LOGS_HOUR = "*"
        if not cls.CLEAR_LOGS_DAY_OF_WEEK:
            cls.CLEAR_LOGS_DAY_OF_WEEK = "*"
        if not cls.CLEAR_LOGS_DAY_OF_MONTH:
            cls.CLEAR_LOGS_DAY_OF_MONTH = "*"
        if not cls.CLEAR_LOGS_MONTH_OF_YEAR:
            cls.CLEAR_LOGS_MONTH_OF_YEAR = "*"

        cls.CLEAR_LOGS_MINUTE_INTERVAL = int(cls.CLEAR_LOGS_MINUTE_INTERVAL)
        cls.CLEAR_LOGS_HOUR_INTERVAL = int(cls.CLEAR_LOGS_HOUR_INTERVAL)
        cls.CLEAR_LOGS_MONTH_INTERVAL = int(cls.CLEAR_LOGS_MONTH_INTERVAL)
        cls.CLEAR_LOGS_YEAR_INTERVAL = int(cls.CLEAR_LOGS_YEAR_INTERVAL)


CeleryLogClearConfig.validate()