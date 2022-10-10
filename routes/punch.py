import settings
from httphelper import Request, Response, STATUS_CODES
from user import User
import re
from socket import socket
import reloadable

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER
session = settings.SESSION_HANDLER

@rh.register(["GET"],"/punch/new")
def routePunchNewGET(req: Request, match: re.Match, sock: socket):
    valid, user = session.validateSession(req=req)
    resp = Response()
    args = {
        'user': user
    }
    resp.body = jinja.get_template("punch/punchNewGET.html").render(**args)
    resp.send(sock)