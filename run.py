from flask import Flask, render_template, request
import psutil
import json
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/publish")
def publish():
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        while True:
            now_ts = int(datetime.now().timestamp())
            cpu_percent_per_core = psutil.cpu_percent(percpu=True)
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(path="/")
            cpu_temp = psutil.sensors_temperatures()['cpu-thermal'][0]
            ws.send(json.dumps([
                {"time": now_ts, "y":cpu_percent_per_core[0]},
                {"time": now_ts, "y":cpu_percent_per_core[1]},
                {"time": now_ts, "y":cpu_percent_per_core[2]},
                {"time": now_ts, "y":cpu_percent_per_core[3]},
                {"time": now_ts, "y":cpu_percent},
                {"time": now_ts, "y":memory.used},
                {"time": now_ts, "y":memory.free},
                {"time": now_ts, "y":memory.percent},
                {"time": now_ts, "y":disk.used},
                {"time": now_ts, "y":disk.free},
                {"time": now_ts, "y":disk.percent},
                {"time": now_ts, "y":cpu_temp.current},
            ]))
            time.sleep(1)
    return


if __name__ == "__main__":
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
