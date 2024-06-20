import time

from fastapi import FastAPI, Request, HTTPException, status


from backend.utils import get_response_body, make_exception_message
from backend.logger import MyLogger
from backend.config import ClickHouseConfig, DEBUG
from backend.models.logs import StatusOK, Status400, Status500


app = FastAPI(debug=DEBUG)
logger = MyLogger(clickhouse_host=ClickHouseConfig.CLICKHOUSE_HOST, clickhouse_port=ClickHouseConfig.CLICKHOUSE_PORT,
                  db_name=ClickHouseConfig.CLICKHOUSE_DB_NAME, db_user=ClickHouseConfig.CLICKHOUSE_USER,
                  db_password=ClickHouseConfig.CLICKHOUSE_PASSWORD, console=DEBUG,
                  name="backend")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    request_body = (await request.body()).decode()
    client_ip = request.client.host + ":" + str(request.client.port)
    process_time = int((time.time() - start_time) * 1000)
    method = request.method
    path = str(request.url)
    response = await call_next(request)
    status = response.status_code
    request_headers = str(request.headers)[8:-1]
    if 200 <= status < 400:
        data = StatusOK(status_code=status, execution_time_ms=process_time,
                        method=method, path=path,
                        request_body=request_body, request_headers=request_headers,
                        client_ip=client_ip)
        logger.info(data)
    else:
        response_body = await get_response_body(response)
        message = "unknown"
        if "detail" in response_body:
            message = response_body["detail"]
        if 400 <= status < 500:
            data = Status400(status_code=status, execution_time_ms=process_time,
                             method=method, path=path,
                             request_body=request_body, request_headers=request_headers,
                             client_ip=client_ip, message=message)
            logger.warning(data)
        else:

            data = Status500(status_code=status, execution_time_ms=process_time,
                             method=method, path=path,
                             request_body=request_body, request_headers=request_headers,
                             client_ip=client_ip, message=message)
            logger.error(data)
            raise Exception(message)
    return response

