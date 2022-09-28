import settings
import httpserver as httpserver
import routes, routes.api
from httphelper import Request, Response
from re import Match
from socket import socket
import importlib
import json
import sys
import html

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT, settings.ROUTE_HANDLER)
rh = settings.ROUTE_HANDLER

@rh.register(["GET"],"/api/reload$")
def reloadRoutes(req: Request, match: Match, sock: socket):
    body = ""
    for k,v in sys.modules.copy().items():
        if "reloadable" in dir(v):
            importlib.reload(v)
    resp = Response()
    data = {
        "action": "reload",
        "result": "success",
        "body": body
    }
    resp.body = json.dumps(data)
    resp.send(sock)

server.start()
server.listenthread.join()