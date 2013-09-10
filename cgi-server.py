#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

class CGIServer(HTTPServer):
    def __init__(self, (hostname,port), handler):
        HTTPServer.__init__(self, (hostname, port), handler)

if __name__ == '__main__':
    srvaddr = ("", 8080) #Computername, Portnummer
    cgisrv = CGIServer(srvaddr,CGIHTTPRequestHandler)
    cgisrv.serve_forever()
