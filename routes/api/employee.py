import re
import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
from socket import socket
import json

session = settings.SESSION_HANDLER
rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["POST"],"/api/employee/new")
def employeeNew(req: Request, match: Match, sock: socket):
    valid, userid = session.validateSession(req)
    resp = Response()
    data = dict()
    data["action"] = req.form["employeeNew"]
    if valid:
        try:
            args = {
                "fname": req.form["fname"].asStr(),
                "lname": req.form["lname"].asStr(),
                "admin": req.form["admin"].asBool()
            }
            e = ec.creatEmployee(**args)
            data["result"] = "success"
            data["employeeid"] = e.id
            data["fname"] = e.fname
            data["lname"] = e.lname
            data["admin"] = e.admin
            data["body"] = f'Successfully created employee: <a href="/employee/{e.id}">{e.lname}, {e.fname}</a>'
        except Exception:
            data["result"] = "fail"
    else:
        data["result"] = "fail"
    resp.body = json.dumps(data)
    resp.send(sock)

@rh.register(["POST"],"/api/employee/edit")
def employeeEdit(req: Request, match: Match, sock: socket):
    pass

@rh.register(["POST"], "/api/employee/delete")
def employeeDelete(req: Request, match: Match, sock: socket):
    pass