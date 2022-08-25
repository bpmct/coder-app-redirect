#!/usr/bin/env python3

# put this in /coder/apps/devurl_redirect.py

import os, sys, re, requests, argparse

from http.server import HTTPServer, BaseHTTPRequestHandler

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--listen-port", dest = "listen_port", default=8888, type=int)
parser.add_argument("-s", "--redirect-to", dest = "redirect_to", default="https://example.com")

args = parser.parse_args()

class Redirect(BaseHTTPRequestHandler):
    def do_HEAD(self):
        # for Coder health checks
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # also for health check
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("All OK", "utf8"))
            return
        
        print ("Redirecting to " + args.redirect_to)
        self.send_response(302)
        self.send_header('Location', args.redirect_to)
        self.end_headers()

print("Starting redirect server on port", args.listen_port)
HTTPServer(("", int(args.listen_port)), Redirect).serve_forever()