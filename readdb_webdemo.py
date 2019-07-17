#from http.server import BaseHTTPRequestHandler, HTTPServer
from http.server import HTTPServer, SimpleHTTPRequestHandler, HTTPStatus
import ssl
import time
import pyodbc

hostName = "localhost"
hostPort = 9000

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Demo Access DB Read Web</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lewisz\Desktop\Database11.accdb;')

        cursor = conn.cursor()

        cursor.execute('select * from demo1')
        self.wfile.write(bytes("<pre>", "utf-8"))
        for row in cursor.fetchall():
            self.wfile.write(bytes("<br>" + str(row),"utf-8"))
        self.wfile.write(bytes("</pre>", "utf-8"))
       
        self.wfile.write(bytes("</body></html>", "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
myServer.socket = ssl.wrap_socket (myServer.socket, certfile='cacert.pem', keyfile='cakey.pem', server_side=True)

#myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))