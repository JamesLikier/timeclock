import settings
from httphelper import Request, Response, STATUS_CODES, CONTENT_TYPES
from user import User
import re
from socket import socket

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
cache = settings.CACHE

@rh.registerstatic("/static/(.*\.(.*)$|.*$)")
def routeStatic(req: Request, match: re.Match, sock: socket):
    urlFilepath = match.group(1)
    paths = tuple(urlFilepath.split("/"))
    f = cache.get(".","static",*paths)
    ext = "" if match.lastgroup == 1 else match.group(2)
    resp = Response(contentType=(CONTENT_TYPES["txt"] if ext not in CONTENT_TYPES else CONTENT_TYPES[ext]))
    if f != None:
        resp.body = f
    else:
        resp.statuscode = STATUS_CODES[404]
        
    resp.send(sock)