import json
from dataclasses import dataclass
from typing import Dict

import websocket

from valsys.utils import logger

TRACE_DEFAULT = False


class States:
    IN_PROGRESS = "INPROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class Status:
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Message:
    status: str
    err: str
    close: bool
    step: str

    @classmethod
    def from_json(cls, response):
        return cls(status=response.get("status"),
                   err=response.get("error"),
                   close=response.get("Close"),
                   step=response.get("step"))

    @classmethod
    def from_response(cls, response):
        return cls.from_json(json.loads(response))


class SocketHandler:

    def __init__(self,
                 url: str,
                 config: Dict[str, str],
                 auth_token: str,
                 trace: bool = TRACE_DEFAULT,
                 after_token=None) -> None:

        self.config = config
        self.error = None
        self.status = Status.UNKNOWN
        self.resp = None
        self.exception = None
        self.state = States.IN_PROGRESS
        # enable trace in dev for debugging
        websocket.enableTrace(trace)
        self.url = url
        logger.debug(f"connecting to socket {self.url}")
        socketpath = f"{self.url}" + auth_token
        if after_token is not None:
            socketpath += '/' + after_token
        self.wsapp = websocket.WebSocketApp(
            url=socketpath,
            on_open=self.send_data,
            on_message=self.msg_handler,
            on_close=self.on_close,
            on_error=self.on_error,
        )

    def send_data(self, ws: websocket.WebSocketApp):
        ws.send(json.dumps(self.config))

    def on_error(self, ws: websocket.WebSocketApp, err: Exception):
        self.state = States.ERROR
        self.exception = err
        logger.error(f"{str(err)} URL={self.url}")

    def msg_handler(self, ws, message):
        # Statuses: success, failed
        # decided if good or bad
        response = json.loads(message)
        status = response.get("status")
        err = response.get("error")
        close = response.get("Close")
        step = response.get("step")
        self.status = status
        self.resp = response
        if not self.succesful:
            self.error = err
            self.status = Status.FAILED
            logger.error(f"from {self.url} {message}")
        if err != "":
            self.error = err
            self.status = Status.FAILED
            self.on_close(ws, websocket.STATUS_NORMAL, message)
        elif close is True:
            self.on_close(ws, websocket.STATUS_NORMAL, message)

    def on_close(self, ws, close_status_code, close_msg):
        self.state = States.COMPLETE
        if close_status_code != websocket.STATUS_NORMAL:
            logger.error(f"close status={close_status_code} msg={close_msg}")
            self.error = 'unknown'
            self.status = Status.FAILED
        elif close_status_code or close_msg:
            logger.debug(f"close status={close_status_code} ")
        ws.close()

    def run(self):
        # ping and pong period to keep socket connection
        pong = 60
        ping = (pong * 9) / 10

        self.wsapp.run_forever(ping_interval=pong,
                               ping_timeout=ping,
                               ping_payload="0x9")

    @property
    def succesful(self):
        return self.status == Status.SUCCESS

    @property
    def complete(self):
        return self.state == States.COMPLETE
