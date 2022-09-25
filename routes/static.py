import settings
from lib.http import Request, Response, STATUS_CODES
from lib.user import User
import re
from socket import socket

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
cache = settings.CACHE

@rh.registerstatic("/static/(.*)$")
def routeStatic(req: Request, match: re.Match, sock: socket):
    resp = Response()
    urlFilepath = match.group(1)
    paths = tuple(urlFilepath.split("/"))

    f = cache.get(".","static",*paths)
    if f != None:
        resp.body = f
    else:
        resp.statuscode = STATUS_CODES[404]
        
    resp.send(sock)