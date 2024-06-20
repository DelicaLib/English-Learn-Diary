import logging

from clickhouse_connect import get_client
from clickhouse_connect.driver.client import Client as ch_client

from backend.database.clickhouse import insert_log
from backend.models.logs import StatusOK, Status400, Status500, BaseTable


class ClickhouseHandler(logging.Handler):
    Client = None

    def __init__(self, clickhouse_client: ch_client, level: int = logging.NOTSET):
        super().__init__(level)
        self.Client = clickhouse_client

    def emit(self, record):
        level = record.levelno
        data = getattr(record, 'data', None)
        if level == logging.INFO:
            insert_log(self.Client, "statusOK", data)
        elif level == logging.WARNING:
            insert_log(self.Client, "status400", data)
        elif level == logging.ERROR:
            insert_log(self.Client, "status500", data)
            print(*data)
        else:
            super().emit(record)


class MyLogger:
    __logger = None
    __console = False
    __client = None

    def __init__(self, clickhouse_host: str,
                 clickhouse_port: int, db_name: str,
                 db_user: str, db_password: str,
                 console: bool = False, name: str = "default"):
        self.__console = console
        try:
            self.__client = get_client(host=clickhouse_host, database=db_name,
                                       user=db_user, password=db_password,
                                       port=clickhouse_port)
        except Exception as ex:
            raise ex

        logger_handler = ClickhouseHandler(self.__client)
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(logger_handler)

        if self.__console:
            self.__logger_console = logging.getLogger(name + " debug")
            self.__logger_console.setLevel(logging.DEBUG)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.__logger_console.addHandler(console_handler)

    def info(self, data: StatusOK):
        extra = {'data': data}
        self.__logger.info("", extra=extra)
        if self.__console:
            self.__logger_console.info(data.message)
            print(str(data))

    def warning(self, data: Status400):
        extra = {'data': data}
        self.__logger.warning("", extra=extra)
        if self.__console:
            self.__logger_console.warning(data.message)
            print(str(data))

    def error(self, data: Status500):
        extra = {'data': data}
        self.__logger.error("", extra=extra)
        if self.__console:
            self.__logger_console.error(data.message)
            print(str(data))

    def debug(self, data: BaseTable):
        if self.__console:
            self.__logger_console.debug(data.message)
            print(str(data))
