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
