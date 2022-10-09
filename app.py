import settings
import httpserver as httpserver
import routes, routes.api
from httphelper import Request, Response
from re import Match
from socket import socket
import importlib
import sys
from routes.api.util import Message

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT, settings.ROUTE_HANDLER)
rh = settings.ROUTE_HANDLER

@rh.register(["GET"],"/api/reload$")
def reloadRoutes(req: Request, match: Match, sock: socket):
    for v in sys.modules.copy().values():
        if "reloadable" in dir(v):
            importlib.reload(v)
    resp = Response()
    msg = Message(action="reload",result=Message.SUCCESS)
    resp.body = msg.toJSON()
    resp.send(sock)

server.start()
server.listenthread.join()