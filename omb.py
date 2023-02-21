import socket
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from appJar import gui
import webbrowser
import threading
import json
import cgi

def server(btn):
    if btn == "Start":
        host_name = socket.gethostbyname(socket.gethostname())
        port_number = 5151
        # Create an HTTP server
        httpd = HTTPServer((host_name, port_number), SimpleHTTPRequestHandler)
        # Start the server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()
        app.setLabel("SL", f"Server: http://{host_name}:{port_number}")
        app.setLabel("SS", "Server is Online")
        print("Server started at http://{}:{}/files".format(*httpd.socket.getsockname()))
def do_upload(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        keep_blank_values=True
    )

    fileitem = form['fileToUpload']
    if fileitem.filename:
        # Make sure the file is saved with a unique name
        filename = os.path.basename(fileitem.filename)
        with open('/files/' + filename, 'wb') as f:
            f.write(fileitem.file.read())
        start_response('200 OK', [('Content-type', 'text/html')])
        return [b'Thanks for uploading!']
    else:
        start_response('400 Bad Request', [('Content-type', 'text/html')])
        return [b'No file was uploaded.']
app=gui("OMB")
app.addLabel("OMB RSLClient")
app.startLabelFrame("Server General Commands")
app.addButtons(["Start","Stop"],server)
app.stopLabelFrame()

app.startLabelFrame("Server Status")
app.addLabel("SL","Server Location:")
app.addLabel("SS","Server Status:")
app.stopLabelFrame()
app.go()