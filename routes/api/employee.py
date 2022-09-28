import re
import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
from socket import socket
import json
import reloadable
from api.apiresponse import APIResponse

session = settings.SESSION_HANDLER
rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["POST"],"/api/employee/new")
def employeeNew(req: Request, match: Match, sock: socket):
    valid, userid = session.validateSession(req=req)
    resp = Response()
    apiResp = APIResponse()
    apiResp.action = "employeeNew"
    if valid:
        try:
            args = {
                "fname": req.form["fname"].asStr(),
                "lname": req.form["lname"].asStr(),
                "admin": True if "admin" in req.form else False
            }
            e = ec.createEmployee(**args)
            apiResp.result = APIResponse.SUCCESS
            apiResp.body = f'Successfully created employee: <a href="/employee/{e.id}">{e.lname}, {e.fname}</a>'
        except Exception:
            apiResp.result = APIResponse.FAIL
            apiResp.body = "Error Encountered"
    else:
        apiResp.result = APIResponse.FAIL
        apiResp.body = "Unauthorized User"
    resp.body = apiResp.toJSON()
    resp.send(sock)

@rh.register(["POST"],"/api/employee/edit")
def employeeEdit(req: Request, match: Match, sock: socket):
    pass

@rh.register(["POST"], "/api/employee/delete")
def employeeDelete(req: Request, match: Match, sock: socket):
    pass