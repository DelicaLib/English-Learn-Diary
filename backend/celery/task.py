import celery

from backend.database.clickhouse import ClickhouseManager


class ClearOldLogTask(celery.Task):
    name = "ClearOldLogTask"
    __clickhouse_manager = None
    __host = None
    __port = None
    __database = None
    __user = None
    __password = None

    def __init__(self, clickhouse_host: str,
                 clickhouse_port: int, db_name: str,
                 db_user: str, db_password: str):
        self.__host = clickhouse_host
        self.__port = clickhouse_port
        self.__database = db_name
        self.__user = db_user
        self.__password = db_password
        super().__init__()

    @property
    def clickhouse_manager(self):
        print("property")
        if self.__clickhouse_manager is None:
            self.__clickhouse_manager = ClickhouseManager(host=self.__host, port=self.__port,
                                                          database=self.__database, user=self.__user,
                                                          password=self.__password)
            print("property_nice")
        print("property_return")
        return self.__clickhouse_manager

    def run(self, *args, **kwargs):
        print("penis")
        self.clickhouse_manager.delete_old_logs("statusOK")
        self.clickhouse_manager.delete_old_logs("status400")
        self.clickhouse_manager.delete_old_logs("status500")

