import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import time

PAGE="""\
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>PiX</title>
  <link rel="icon" type="image/x-icon" href="https://www.spacex.com/sites/all/themes/spacex2012/favicon.ico">

  <style>

    @import url(https://fonts.googleapis.com/css?family=Inconsolata);

    html {
      background: url('stream.mjpg') fixed;
      background-size: 100%;
    }

    body {
      height:100%;
      width:285px;
      font-family: 'Inconsolata', monospace;
    }

    div {
      overflow: hidden;
    }

    #telemetry {
      position: relative;
      height: 380px;
      width: 285px;
      padding: 4px;
      overflow: hidden;
      background: rgba(255, 255, 255, .2);
    }
    #telemetry #numericItems {
      width: 99%;
      height: 20%;
      float: left;
      list-style: none;
      padding: 0;
      margin: 0;
    }
    #telemetry #numericItems li {
      position: relative;
      float: left;
      width: 100%;
      font-size: 12pt;
      color: rgba(255, 255, 255, .6);
    }
    #telemetry #numericItems #timeDisplay {
      text-align: center;
    }
    #telemetry #visualItems {
      width: 100%;
      height: 80%;
      float: left;
      list-style: none;
      padding: 0;
      margin: 0;
    }
    #telemetry #visualItems li {
      position: relative;
      float: left;
      width: 100%;
      height: 50%;
      font-size: 12pt;
      color: rgba(255, 255, 255, .6);
      border-top: 1px solid gray;
    }
    #telemetry #visualItems li p {
      height: 5%;
      margin: 0;
      text-align: center;
    }
    #telemetry #visualItems li div {
      height: 95%;
      margin: 0;
    }

  </style>
</head>

<body>

  <div>
    <div id="telemetry">
      <ul id="numericItems">
        <li id="timeDisplay"></li>
        <li>Altitude: </li>
        <li>Pressure: </li>
        <li>Temperature: </li>
      </ul>
      <ul id="visualItems">
        <li>
          <p>Accelerometer</p>
          <div></div>
        </li>
        <li>
          <p>Gyroscope</p>
          <div></div>
        </li>
      </ul>
    </div>
  </div>

  <script>
    var ws = new WebSocket("ws://192.168.0.8:8001/");
    ws.onmessage = function (event) {
      var timeDisplay = document.getElementById('timeDisplay'),
          timeData = document.createTextNode(event.data);
      timeDisplay.innerHTML = timeData.textContent.concat(" UTC");
    };
  </script>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        #elif self.path == '/temperature.txt':
        #    self.send_response(200)
        #    try:
        #        while True:
        #             with open("temperature.txt", "r+") as f:
        #                f.seek(0)
        #                f.write("{:.3f}".format(bmp280.get_temperature()) + "C")
        #                f.truncate()
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
