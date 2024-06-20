from clickhouse_connect.driver.client import Client
from backend.models.logs import BaseTable


def insert_log(client: Client, table_name: str, data: BaseTable):
    col_names = []
    col_data = []
    for i in [*data]:
        col_names.append(i[0])
        col_data.append(i[1])
    client.insert(table=table_name, data=[col_data], column_names=col_names)
