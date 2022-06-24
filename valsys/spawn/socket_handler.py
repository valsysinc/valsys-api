import json
from typing import Dict
import websocket
from valsys.config import SCK_MODELING_CREATE
from valsys.utils import logger


class States:
    IN_PROGRESS = "INPROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class Status:
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILED = "failed"


class SocketHandler:
    def __init__(self, config: Dict[str, str], auth_token: str, trace=False) -> None:

        self.config = config
        self.error = None
        self.status = Status.UNKNOWN
        self.resp = None
        self.exception = None
        self.state = States.IN_PROGRESS
        # enable trace in dev for debugging
        websocket.enableTrace(trace)
        logger.debug(f"connecting to socket {SCK_MODELING_CREATE}")
        socketpath = f"{SCK_MODELING_CREATE}" + auth_token
        self.wsapp = websocket.WebSocketApp(
            url=socketpath,
            on_open=self.create_model,
            on_message=self.msg_handler,
            on_close=self.on_close,
            on_error=self.on_error,
        )

    def create_model(self, ws: websocket.WebSocketApp):
        ws.send(json.dumps(self.config))

    def on_error(self, ws: websocket.WebSocketApp, err: Exception):
        self.state = States.ERROR
        self.exception = err
        logger.error(f"{str(err)} URL={SCK_MODELING_CREATE}")

    def msg_handler(self, ws, message):
        # Statuses: success, failed
        # decided if good or bad
        response = json.loads(message)
        status = response.get("status")
        err = response.get("error")
        close = response.get("Close")
        step = response.get("step")
        self.status = status

        if status != Status.SUCCESS:
            self.error = response["error"]
            self.status = Status.FAILED
            logger.error(f"from {SCK_MODELING_CREATE} {message}")
        if err != "":
            self.error = response["error"]
            self.status = Status.FAILED
            self.on_close(ws, websocket.STATUS_NORMAL, message)
        elif close is True:
            self.resp = response
            self.on_close(ws, websocket.STATUS_NORMAL, message)

    def on_close(self, ws, close_status_code, close_msg):
        self.state = States.COMPLETE
        if close_status_code != websocket.STATUS_NORMAL:
            logger.error(f"close status={close_status_code} msg={close_msg}")
        elif close_status_code or close_msg:
            logger.debug(f"close status={close_status_code} ")
        ws.close()

    def run(self):
        # ping and pong period to keep socket connection
        pong = 60
        ping = (pong * 9) / 10

        self.wsapp.run_forever(
            ping_interval=pong, ping_timeout=ping, ping_payload="0x9"
        )

    @property
    def succesful(self):
        return self.status == Status.SUCCESS

    @property
    def complete(self):
        return self.state == States.COMPLETE
