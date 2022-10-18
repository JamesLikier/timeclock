import settings
import jlpyhttp.httpserver as httpserver
import routes, routes.api
from jlpyhttp.sessionhandler import SessionHandler
from jlpyhttp.httphelper import Request, Response
from re import Match
import importlib
import sys
from routes.api.util import Message

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT, settings.ROUTE_HANDLER)
rh = settings.ROUTE_HANDLER

@rh.register(["GET"],"/api/reload$")
def reloadRoutes(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    for v in sys.modules.copy().values():
        if "reloadable" in dir(v):
            importlib.reload(v)
    
    msg = Message(action="reload",result=Message.SUCCESS)
    resp.body = msg.toJSON()
    resp.send()

server.start()
server.listenthread.join()