from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import subprocess
import json
import daemon

class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        # create and send headers                                                                                                                                                                                                      
        self.send_response(200)                                                                                                                                                                                                        
        self.send_header('Content-type', 'application/json')                                                                                                                                                                           
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
	# get resuls
        res = subprocess.check_output(["status", "-h", "mobile", "1"])   
        res = res.decode('utf-8').strip()                                
        res = dict([ [ item.strip() for item in ttuple.split(":")] for ttuple in res.split("\n")])	

        # return json
        self.wfile.write(json.dumps(res).encode())

if __name__ == "__main__":
    from sys import argv

    port = 50000

    server_address = ('', port)                        
    server = HTTPServer(server_address, MyHttpRequestHandler)

    # Make the context manager for becoming a daemon process.
    daemon_context = daemon.DaemonContext()
    daemon_context.files_preserve = [server.fileno()]

    # Become a daemon process.
    with daemon_context:
        server.serve_forever()
