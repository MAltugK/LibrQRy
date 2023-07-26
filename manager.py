from http.server import BaseHTTPRequestHandler, HTTPServer

# HTML template for the webpage
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
            width: 100px;
            height: 100px;
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
    <script>
        function updateBoxes(data) {
            const boxElements = document.querySelectorAll('.redbox');
            for (let i = 0; i < boxElements.length; i++) {
                if (data.includes((i + 1).toString())) {
                    boxElements[i].classList.add('greenbox');
                    boxElements[i].classList.remove('redbox');
                } else {
                    boxElements[i].classList.add('redbox');
                    boxElements[i].classList.remove('greenbox');
                }
            }
        }

        const eventSource = new EventSource('/events');
        eventSource.onmessage = function (event) {
            updateBoxes(event.data);
        };
    </script>
</body>
</html>
"""

# Global variable to store the state of the boxes
box_state = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]


class QRCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/manager':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(manager_template.encode())



def run():
    try:
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, QRCodeHandler)
        print("Starting Manager server...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Manager server...")
        httpd.socket.close()


if __name__ == '__main__':
    run()
