import datetime
import json

from starlette.concurrency import iterate_in_threadpool


async def get_response_body(response) -> dict:
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    response_body_json = response_body[0].decode()
    try:
        return json.loads(response_body_json)
    except Exception as ex:
        return {"detail": "unknown"}


def get_current_time() -> datetime.datetime:
    return datetime.datetime.now()


def make_exception_message(ex: Exception, file_name: str,
                           func_name: str, detail: str = ""):
    return f"""Exception: {type(ex).__name__}
File name: {file_name}
Func name: {func_name}
Detail: {str(ex)}. {detail}
"""
