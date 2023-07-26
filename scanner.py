import http.server
import time
from pyzbar.pyzbar import decode
from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2


# HTML template for the webpage
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Code Scanner</title>
</head>
<body>
    <h1>QR Code Scanner</h1>
    <img src="stream" width="640" height="480" />
    <div id="qr_data"></div>
</body>
<script>
    function updateQRData(data) {
        document.getElementById('qr_data').innerText = data;
    }

    function handleEvent(event) {
        if (event.target instanceof EventSource) {
            event.target.onmessage = function (event) {
                updateQRData(event.data);
            };
        }
    }

    handleEvent(new Event('DOMContentLoaded'));
</script>
</html>
"""

manager_template = """<!DOCTYPE html>
<html>
<head>
    <title>4x4 Red Boxes</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            display: grid;
            grid-template-columns: repeat(4, 100px);
            grid-template-rows: repeat(4, 100px);
            gap: 5px;
        }

        .redbox {
            width: 100px;
            height: 100px;
            background-color: red;
        }

        .greenbox {
            background-color: green;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
        <div class="redbox"></div>
    </div>
</body>
</html>
"""
# Global variable to store QR code data
qr_data = ""


# Define the HTTP request handler class
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def change_box_color(self, color):
        box_index = self.server.box_index % 16  # Limit the index to 0-15
        self.server.box_index += 1  # Increment the index for the next QR code
        self.wfile.write(
            f'<script>document.getElementsByClassName("box")[{box_index}].style.backgroundColor = "{color}";</script>'.encode())

    def camera_stream(self):
        # Open the default camera
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to a byte array
            _, frame_buffer = cv2.imencode('.jpg', frame)
            frame_bytes = frame_buffer.tobytes()

            # Send the frame as multipart response
            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-length', len(frame_bytes))
            self.end_headers()
            self.wfile.write(frame_bytes)
            self.wfile.write(b'\r\n')

            # Attempt to detect QR codes
            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                print(f"Detected QR code: {qr_data}")
                self.update_box_colors(qr_data)
                time.sleep(3)

        cap.release()


    def do_GET(self):
        if self.path == '/manager':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(manager_template.encode())
        elif self.path == '/scanner':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_template.encode())
        elif self.path == '/stream':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            self.camera_stream()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Page not found</h1></body></html>")

    def update_box_colors(self, qr_datum):
        # Get the numeric value from the QR code
        num = int(qr_datum)

        # Update the box color based on the numeric value
        for i in range(1, 17):
            box_class = f".box{i}"
            if i <= num:
                new_class = "greenbox"
            else:
                new_class = "redbox"
            self.send_message(f"document.querySelector('{box_class}').classList.remove('redbox');")
            self.send_message(f"document.querySelector('{box_class}').classList.remove('greenbox');")
            self.send_message(f"document.querySelector('{box_class}').classList.add('{new_class}');")

    def send_message(self, message):
        self.wfile.write(f"data: {message}\n\n".encode())


# Define the function to start the server
def run():
    try:
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, MyRequestHandler)
        httpd.box_index = 0  # Initialize the box index in the server instance
        print("Starting QR Code Scanner server...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping QR Code Scanner server...")
        httpd.socket.close()


if __name__ == '__main__':
    run()
