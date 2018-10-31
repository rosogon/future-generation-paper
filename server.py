#!/usr/bin/env python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import argparse
from time import sleep
import random

index = 0

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global args
        global index

        alive = 1 if (args.pattern[index] != '0') else 0
        
        index = (index + 1) % len(args.pattern)

        t = random.randint(args.min, args.max)
        sleep(t / 1000)
        
        self.send_response(200 if alive else 500)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("Alive: {} Delay time: {}".format(alive, t))
        return


def main(args):
    port = args.port

    if args.template is None:
        args.pattern = "1"
    else:
        args.pattern = args.template.format(1, 0)
    print('Running with pattern {}'.format(args.pattern))
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", default=8020, type=int, metavar="port", dest="port")
    parser.add_argument("-m", default=0, type=int, metavar="min rt", dest="min", help="Minimum response time of a request")
    parser.add_argument("-M", default=0, type=int, metavar="max rt", dest="max", help="Maximum response time of a request")
    parser.add_argument("-t", default="1", type=str, metavar="template", dest="template", help="Template to construct the alive pattern. Ex: '{:1<30}0'")

    args = parser.parse_args()
    
    main(args)
