import settings
from httphelper import Request, Response, STATUS_CODES
from user import User
import re
from socket import socket
import reloadable

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["GET"], "/employee/([0-9]+)$")
def routeEmployee(req: Request, match: re.Match, sock: socket):
    resp = Response()
    user = User.fromSession(req)
    if user is not None:
        employee = ec.getEmployeeById(int(match.group(1)))
        args = {
            "user": user,
            "employee": employee
        }
        resp.body = jinja.get_template("employee/employee.html").render(**args)
    else:
        resp.body = jinja.get_template("user/login_required.html").render()
    resp.send(sock)

@rh.register(["POST"], "/employee/new$")
def routeEmployeeNewPOST(req: Request, match: re.Match, sock: socket):
    resp = Response()
    user = User.fromSession(req)
    if user is not None:
        e = ec.createEmployee(fname=req.form.data["fname"].asStr(),
                                            lname=req.form.data["lname"].asStr(),
                                            admin=req.form.data["admin"].asBool())
        args = {
            "user": user,
            "employee": e
        }
        resp.body = jinja.get_template("employee/employeeNewPOST.html").render(**args)
    else:
        resp.body = jinja.get_template("user/login_required.html").render()
    resp.send(sock)

@rh.register(["GET"], "/employee/new$")
def routeEmployeeNewGET(req: Request, match: re.Match, sock: socket):
    resp = Response()
    user = User.fromSession(req)
    if user is not None:
        args = {
            "user": user
        }
        resp.body = jinja.get_template("employee/employeeNewGET.html").render(**args)
    else:
        resp.body = jinja.get_template("user/login_required.html").render()
    resp.send(sock)

@rh.register(["GET"], r"/employee/list$|/employee/list\?(\&?(pg|pgSize)=([0-9]+))(\&?(pg|pgSize)=([0-9]+))")
def routeEmployeeList(req: Request, match: re.Match, sock: socket):
    resp = Response()
    user = User.fromSession(req)
    if user is not None:
        pg = int(match.group(3) or 1) if match.group(2) == 'pg' else int(match.group(6) or 1)
        pgSize = int(match.group(6) or 20) if match.group(2) == 'pg' else int(match.group(3) or 20)
        employees = ec.getEmployeeList(offset=(pg-1)*pgSize,count=pgSize)
        args = {
            "user": user,
            "pg": pg,
            "pgSize": pgSize,
            "employees": employees,
            "displayCount": len(employees),
            "totalEmployees": len(ec.employeeDict)
        }
        resp.body = jinja.get_template("employee/employeeList.html").render(**args)
    else:
        resp.body = jinja.get_template("user/login_required.html").render()
    resp.send(sock)