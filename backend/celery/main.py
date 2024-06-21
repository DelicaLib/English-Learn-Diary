import celery

from backend.celery.task import ClearOldLogTask
from backend.config import ClickHouseConfig


app = celery.Celery("tasks")
app.config_from_object("backend.celery.config")

app.register_task(ClearOldLogTask(ClickHouseConfig.CLICKHOUSE_HOST, ClickHouseConfig.CLICKHOUSE_PORT,
                                  ClickHouseConfig.CLICKHOUSE_DB_NAME, ClickHouseConfig.CLICKHOUSE_USER,
                                  ClickHouseConfig.CLICKHOUSE_PASSWORD))


if __name__ == "__main__":
    app.start()
