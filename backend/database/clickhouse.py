from backend.models.logs import BaseTable
from clickhouse_connect import get_client

from backend.config import CeleryLogClearConfig


class ClickhouseManager:
    __client = None

    def __init__(self, host: str,
                 port: int, database: str,
                 user: str, password: str):
        try:
            self.__client = get_client(host=host, database=database,
                                       user=user, password=password,
                                       port=port)
        except Exception as ex:
            raise ex

    def insert_log(self, table_name: str, data: BaseTable):
        col_names = []
        col_data = []
        for i in [*data]:
            col_names.append(i[0])
            col_data.append(i[1])
        self.__client.insert(table=table_name, data=[col_data], column_names=col_names)

    def delete_old_logs(self, table_name: str):
        query = f"""ALTER TABLE {table_name} DELETE WHERE 
    timestamp < toDateTime(
        now() - interval {CeleryLogClearConfig.CLEAR_LOGS_YEAR_INTERVAL} year - 
        interval {CeleryLogClearConfig.CLEAR_LOGS_MONTH_INTERVAL} month - 
        interval {CeleryLogClearConfig.CLEAR_LOGS_DAY_INTERVAL} day - 
        interval {CeleryLogClearConfig.CLEAR_LOGS_HOUR_INTERVAL} hour - 
        interval {CeleryLogClearConfig.CLEAR_LOGS_MINUTE_INTERVAL} minute)"""

        self.__client.command(query)
