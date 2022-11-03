import settings
from jlpyhttp.http import Request, Response, STATUS_CODES, CONTENT_TYPES
from re import Match
from jlpyhttp.sessionhandler import SessionHandler
import reloadable

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
cache = settings.CACHE

@rh.registerstatic(r"/static/(.*\.(.*)$|.*$)")
def routeStatic(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    urlFilepath = match.group(1)
    paths = tuple(urlFilepath.split("/"))
    f = cache.get(".","static",*paths)
    ext = "" if match.lastgroup == 1 else match.group(2)
    resp.headers["Content-Type"] = (CONTENT_TYPES["txt"] if ext not in CONTENT_TYPES else CONTENT_TYPES[ext])
    if f != None:
        resp.body = f
    else:
        resp.statuscode = STATUS_CODES[404]
        
    resp.send()