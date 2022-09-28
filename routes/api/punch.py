import re
import settings
import reloadable
from httphelper import Request, Response, STATUS_CODES, CONTENT_TYPES
from re import Match
from socket import socket
from timeclock import PunchController, Punch, EmployeeController, Employee
import json
from api.apiresponse import APIResponse

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
session = settings.SESSION_HANDLER
pc = settings.PUNCH_CONTROLLER

@rh.register(["POST"],"/api/punch/new")
def punchNew(req: Request, match: Match, sock: socket):
    valid, userid = session.validateSession(req=req)
    apiResp = APIResponse()
    apiResp.action = "punchNew"
    if valid: 
        apiResp.result = APIResponse.SUCCESS
    else:
        apiResp.result = APIResponse.FAIL
    resp = Response()
    resp.body = apiResp.toJSON()
    resp.send(sock)

@rh.register(["GET"],"/api/punch/new")
def punchNew(req: Request, match: Match, sock: socket):
    pass