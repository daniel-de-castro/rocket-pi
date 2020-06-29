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

	<title>RocketPi</title>
	<link rel="icon" type="image/x-icon" href="https://www.spacex.com/static/images/favicon.ico">

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
			height: 480px;
			/*width: 285px;*/
			padding: 4px;
			overflow: hidden;
			border-radius: 1px 5px 5px 1px;
			background: rgba(0, 0, 0, .5);
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
			height: 33%;
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
				<li id="altitudeDisplay"></li>
				<li id="temperatureDisplay"></li>
				<li id="pressureDisplay"></li>
			</ul>
			<ul id="visualItems">
				<li>
					<p>Accelerometer</p>
					<div id="accelChartContainer" style="height: 110px; width: 100%; border-radius: 5px; margin-top: 10px;"></div>
				</li>
				<li>
					<p>Gyroscope</p>
					<div id="gyroChartContainer" style="height: 110px; width: 100%; border-radius: 5px; margin-top: 10px;"></div>
				</li>
				<li>
					<p>Magnetometer</p>
					<div id="magChartContainer" style="height: 110px; width: 100%; border-radius: 5px; margin-top: 10px;"></div>
				</li>
			</ul>
		</div>
	</div>

	<script>

	var accel = [];
	var gyro = [];
	var mag = [];

	window.onload = function () {

		var accelX = [];
		var accelY = [];
		var accelZ = [];

		var accelChart = new CanvasJS.Chart("accelChartContainer", {
			zoomEnabled: true,
			backgroundColor: "transparent",
			axisX:{
				labelFontColor: "transparent"
			},
			axisY:{
				labelFontColor: "#bbbbbb",
				includeZero: false
			},
			toolTip: {
				shared: true
			},
			legend: {
				cursor:"pointer",
				verticalAlign: "top",
				fontSize: 11,
				fontColor: "#bbbbbb",
				itemclick : toggleAccelProperty
			},
			data: [
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					xValueFormatString: "",
					showInLegend: true,
					name: "X",
					dataPoints: accelX
				},
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					showInLegend: true,
					name: "Y" ,
					dataPoints: accelY
				},
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					showInLegend: true,
					name: "Z",
					dataPoints: accelZ
				}
			]
		});

		function toggleAccelProperty(e) {
			if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
				e.dataSeries.visible = false;
			}
			else {
				e.dataSeries.visible = true;
			}
		
			accelChart.render();
		}

		var gyroX = [];
		var gyroY = [];
		var gyroZ = [];

		var gyroChart = new CanvasJS.Chart("gyroChartContainer", {
			zoomEnabled: true,
			backgroundColor: "transparent",
			axisX:{
				labelFontColor: "transparent"
			},
			axisY:{
				labelFontColor: "#bbbbbb",
				includeZero: false
			},
			toolTip: {
				shared: true
			},
			legend: {
				cursor:"pointer",
				verticalAlign: "top",
				fontSize: 11,
				fontColor: "#bbbbbb",
				itemclick : toggleGyroProperty
			},
			data: [
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					xValueFormatString: "",
					showInLegend: true,
					name: "X",
					dataPoints: gyroX
				},
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					showInLegend: true,
					name: "Y" ,
					dataPoints: gyroY
				},
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					showInLegend: true,
					name: "Z",
					dataPoints: gyroZ
				}
			]
		});

		function toggleGyroProperty(e) {
			if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
				e.dataSeries.visible = false;
			}
			else {
				e.dataSeries.visible = true;
			}
		
			gyroChart.render();
		}

		var magX = [];
		var magY = [];
		var magZ = [];

		var magChart = new CanvasJS.Chart("magChartContainer", {
			zoomEnabled: true,
			backgroundColor: "transparent",
			axisX:{
				labelFontColor: "transparent"
			},
			axisY:{
				labelFontColor: "#bbbbbb",
				includeZero: false
			},
			toolTip: {
				shared: true
			},
			legend: {
				cursor:"pointer",
				verticalAlign: "top",
				fontSize: 11,
				fontColor: "#bbbbbb",
				itemclick : toggleMagProperty
			},
			data: [
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					xValueFormatString: "",
					showInLegend: true,
					name: "X",
					dataPoints: magX
				},
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					showInLegend: true,
					name: "Y" ,
					dataPoints: magY
				},
				{
					type: "line",
					xValueType: "dateTime",
					yValueFormatString: "####.00",
					showInLegend: true,
					name: "Z",
					dataPoints: magZ
				}
			]
		});

		function toggleMagProperty(e) {
			if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
				e.dataSeries.visible = false;
			}
			else {
				e.dataSeries.visible = true;
			}
		
			magChart.render();
		}

		var maxDisplayPoints = 60; // updates every second, so will show the last minute
		var updateInterval = 1000; // ms

		// Initial values

		var accelXval = 0;
		var accelYval = 0;
		var accelZval = 0;

		var gyroXval = 0;
		var gyroYval = 0;
		var gyroZval = 0;

		var gyroXval = 0;
		var gyroYval = 0;
		var gyroZval = 0;

		var time = new Date;
		time.setHours(1);
		time.setMinutes(00);
		time.setSeconds(00);
		time.setMilliseconds(00);

		function updateChart(count) {
			count = count || 5;
			time.setTime(time.getTime() + updateInterval);

			accelXval = parseFloat(accel[0]);
			accelYval = parseFloat(accel[1]);
			accelZval = parseFloat(accel[2]);

			// Push the updated values
			accelX.push({
				x: time.getTime(),
				y: accelXval
			});
			accelY.push({
				x: time.getTime(),
				y: accelYval
			});
			accelZ.push({
				x: time.getTime(),
				y: accelZval
			});

			if (accelX.length > maxDisplayPoints) {
				accelX.shift();
				accelY.shift();
				accelZ.shift();
			}

			gyroXval = parseFloat(gyro[0]);
			gyroYval = parseFloat(gyro[1]);
			gyroZval = parseFloat(gyro[2]);

			gyroX.push({
				x: time.getTime(),
				y: gyroXval
			});
			gyroY.push({
				x: time.getTime(),
				y: gyroYval
			});
			gyroZ.push({
				x: time.getTime(),
				y: gyroZval
			});

			if (gyroX.length > maxDisplayPoints) {
				gyroX.shift();
				gyroY.shift();
				gyroZ.shift();
			}

			magXval = parseFloat(mag[0]);
			magYval = parseFloat(mag[1]);
			magZval = parseFloat(mag[2]);

			magX.push({
				x: time.getTime(),
				y: magXval
			});
			magY.push({
				x: time.getTime(),
				y: magYval
			});
			magZ.push({
				x: time.getTime(),
				y: magZval
			});

			if (magX.length > maxDisplayPoints) {
				magX.shift();
				magY.shift();
				magZ.shift();
			}
			
			accelChart.render();
			gyroChart.render();
			magChart.render();
		}

		setInterval(function(){updateChart(5, "accel")}, updateInterval);
	}

	var ws = new WebSocket("ws://192.168.0.8:8001/");
	ws.onmessage = function (event) {
		var timeData = document.createTextNode(event.data).textContent.split('|')[0] + " UTC",
			timeDisplay = document.getElementById('timeDisplay'),
			altitudeData = document.createTextNode(event.data).textContent.split('|')[1] + " m",
			altitudeDisplay = document.getElementById('altitudeDisplay'),
			temperatureData = document.createTextNode(event.data).textContent.split('|')[2] + " C",
			temperatureDisplay = document.getElementById('temperatureDisplay'),
			pressureData = document.createTextNode(event.data).textContent.split('|')[3] + " hPa",
			pressureDisplay = document.getElementById('pressureDisplay'),
			accelData = document.createTextNode(event.data).textContent.split('|')[4],
			gyroData = document.createTextNode(event.data).textContent.split('|')[5],
			magData = document.createTextNode(event.data).textContent.split('|')[6];
		timeDisplay.innerHTML = timeData;
		altitudeDisplay.innerHTML = "Altitude: " + altitudeData;
		temperatureDisplay.innerHTML = "Temperature: " + temperatureData;
		pressureDisplay.innerHTML = "Pressure: " + pressureData;
		accel = accelData.split(',');
		gyro = gyroData.split(',');
		mag = magData.split(',');
	};
	</script>
	<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
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
