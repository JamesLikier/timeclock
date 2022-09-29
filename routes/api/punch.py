import re
import settings
import reloadable
from httphelper import Request, Response, STATUS_CODES, CONTENT_TYPES
from re import Match
from socket import socket
from timeclock import PunchController, Punch, EmployeeController, Employee
import json
from routes.api.util import Message

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
session = settings.SESSION_HANDLER
pc = settings.PUNCH_CONTROLLER

@rh.register(["POST"],"/api/punch/new")
def punchNew(req: Request, match: Match, sock: socket):
    valid, userid = session.validateSession(req=req)
    msg = Message()
    msg.action = "punchNew"
    if valid: 
        msg.result = Message.SUCCESS
    else:
        msg.result = Message.FAIL
    resp = Response()
    resp.body = msg.toJSON()
    resp.send(sock)

@rh.register(["GET"],"/api/punch/new")
def punchNew(req: Request, match: Match, sock: socket):
    pass