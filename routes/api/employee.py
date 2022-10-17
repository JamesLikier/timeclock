import re
import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
from socket import socket
import json
import reloadable
from routes.api.util import Message

session = settings.SESSION_HANDLER
rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["POST"],"/api/employee/new")
def employeeNew(req: Request, match: Match, sock: socket):
    valid, userid = session.validateSession(req=req)
    resp = Response()
    msg = Message()
    msg.action = "employee/new"
    if valid:
        try:
            data = json.loads(req.body)
            args = {
                "username": data['username'],
                "fname": data['fname'],
                "lname": data['lname'],
                "admin": True if "admin" in data else False
            }
            e = ec.createEmployee(**args)
            msg.result = Message.SUCCESS
            msg.body = f'Successfully created employee: <a href="/employee/{e.id}">{e.lname}, {e.fname}</a>'
        except Exception:
            msg.result = Message.FAIL
            msg.body = "Error Encountered"
    else:
        msg.result = Message.FAIL
        msg.body = "Unauthorized User"
    resp.body = msg.toJSON()
    resp.send(sock)

@rh.register(["POST"],"/api/employee/edit")
def employeeEdit(req: Request, match: Match, sock: socket):
    pass

@rh.register(["POST"], "/api/employee/delete")
def employeeDelete(req: Request, match: Match, sock: socket):
    pass