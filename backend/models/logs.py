import datetime

from pydantic import BaseModel, Field

from backend.utils import get_current_time


class BaseTable(BaseModel):
    status_code: int
    timestamp: datetime.datetime = Field(default_factory=get_current_time)
    execution_time_ms: int
    method: str
    path: str
    request_body: str
    client_ip: str
    message: str
    request_headers: str

    def __str__(self):
        return f"""status_code: {self.status_code}
timestamp: {self.timestamp}
execution_time_ms: {self.execution_time_ms}
method: {self.method}
path: {self.path}
request_body: {self.request_body}
request_headers: {self.request_headers}
client_ip: {self.client_ip}
message: {self.message}"""


class StatusOK(BaseTable):
    status_code: int = Field(ge=100, lt=400)
    message: str = Field(default="OK")


class Status400(BaseTable):
    status_code: int = Field(ge=400, lt=500)


class Status500(BaseTable):
    status_code: int = Field(ge=500)


if __name__ == "__main__":
    tmp = StatusOK(status_code=300, timestamp=None,
                   execution_time_ms=200, method="GET",
                   path="/", request_body="['sex', 'loh']",
                   request_headers="[{'dwfwe':'fewfw', 'fwef':'23r23c'}]", client_ip="127.0.0.1",
                   message="OK")
    col_names = []
    col_data = []
    for i in [*tmp]:
        col_names.append(i[0])
        col_data.append(i[1])
    print(col_names)
    print(col_data)
