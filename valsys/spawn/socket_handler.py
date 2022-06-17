import json
import websocket
from valsys.config import URL_MODELING_CREATE 

class SocketHandler:
    def __init__(self, config, auth_token) -> None:
        self.config = config
        self.error = None
        self.timeout = False
        self.resp = None
        self.state = "INPROGRESS"
        # enable trace in dev for debugging
        websocket.enableTrace(False)
        socketpath = f"{URL_MODELING_CREATE}" +auth_token
        self.wsapp = websocket.WebSocketApp(socketpath, 
            on_open=self.create_model,
            on_message=self.msg_hanlder, 
            on_close=self.on_close,
        )
  
    def create_model(self, ws):
        ws.send(json.dumps(self.config))

    def msg_hanlder(self, ws, message):
        response = json.loads(message)
        print(response["status"], response["step"])
        err = response.get("error")
        close = response.get("Close")
        if err != "":
            self.error = response["error"]
            self.on_close(ws, 1000, message)
        elif close == True:
            self.resp = response
            self.on_close(ws, 1000, message)

    def on_close(self, ws, close_status_code, close_msg):
        self.state = "COMPLETE"
        if close_status_code != 1000:
          print(close_status_code, close_msg)
          print("i/o network timeout, will retry")
          self.timeout = True
        elif close_status_code or close_msg:
            print("close status code: " + str(close_status_code))
        ws.close()

    def run(self):
        # ping and pong period to keep socket connection
        pong = 30
        ping = (pong * 9) / 10
        self.wsapp.run_forever(ping_interval=pong, ping_timeout=ping, ping_payload="ping")
    