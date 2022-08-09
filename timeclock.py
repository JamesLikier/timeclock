from lib.httpserver import httpserver,httprequest,httpresponse,statuscodes
import time
from socket import socket

server = httpserver("localhost",80)

@server.registerstatic("/static/.*")
def routeStatic(req: httprequest, sock: socket):
    with open(f"./{req.uri}", 'rb') as f:
        resp = httpresponse(statuscodes.OK)
        resp.body = f.read()
        sock.send(resp.format())

@server.register(("GET",),"/$")
def routeRoot(req: httprequest, sock: socket):
    with open('index.html','rb') as f:
        resp = httpresponse(statuscodes.OK)
        resp.body = f.read()
        sock.send(resp.format())

server.start()
while(True):
    time.sleep(1)