import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
'''

$ curl -XPOST -d '{ "hoge" : 1, "bar" : "bar" }' http://localhost:8080
'''
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print('type of self.path', type(self.path))
        print(self.path)
        try:
            content_len=int(self.headers.get('content-length'))
            requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
            response = { 'status' : 200,
                         'result' : { 'hoge' : 100,
                                      'bar' : 'bar' }
                       }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))
        except Exception as ex:
            print("The information of error is as following")
            print(type(ex))
            print(ex.args)
            print(ex)
            response = { 'status' : 500,
                         'msg' : 'An error occured' }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))
def importargs():
    parser = argparse.ArgumentParser("This is the simple server")
    parser.add_argument('--host', '-H', required=False, default='localhost')
    parser.add_argument('--port', '-P', required=False, type=int, default=8080)
    args = parser.parse_args()
    return args.host, args.port
def run(server_class=HTTPServer, handler_class=MyHandler, server_name='localhost', port=8080):
    server = server_class((server_name, port), handler_class)
    server.serve_forever()
def main():
    host, port = importargs()
    run(server_name=host, port=port)
if __name__ == '__main__':
    main()
#[EOF]