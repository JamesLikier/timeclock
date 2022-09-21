import lib.httpserver as httpserver
import time
from socket import socket
import FileBasedControllers as fbc
import lib.timeclock as tc
from re import Match
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from lib.cachedfilemanager import CachedFileManager
import logging
import lib.auth as auth

server = httpserver.Server("10.0.0.100",80)
employeeController: tc.EmployeeController = fbc.FileBasedEmployeeController("employeefile")
punchController: tc.PunchController = fbc.FileBasedPunchController("punchfile")
cache = CachedFileManager()
authHandler = auth.AuthHandler()

logging.basicConfig(filename="timeclock.log", filemode="w", level=logging.DEBUG)

env = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
env.filters["floor"] = lambda val, floor: val if val > floor else floor
env.filters["ceil"] = lambda val, ceil: val if val < ceil else ceil

def getUserFromSession(req: Request) -> Employee or None:
    user = None
    valid, userid = authHandler.validateSession(req)
    if valid:
        user = employeeController.getEmployeeById(userid)
    return user

@server.register404
def timeclock404(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    resp.statuscode = httpserver.STATUS_CODES[404]
    resp.body = b'404 - Not Found'
    resp.send(sock)

@server.registerstatic("/static/(.*)$")
def routeStatic(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    urlFilepath = match.group(1)
    paths = tuple(urlFilepath.split("/"))

    f = cache.get(".","static",*paths)
    if f != None:
        resp.body = f
    else:
        resp.statuscode = httpserver.STATUS_CODES[404]
        
    resp.send(sock)

@server.register(["GET"],"/$")
def routeRoot(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    user = getUserFromSession(req)
    template = env.get_template("index.html")
    args = {
        "user": user
    }
    resp.body = template.render(**args)
    resp.send(sock)

@server.register(["GET"], "/employee/([0-9]+)$")
def routeEmployee(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    template = env.get_template("employee.html")
    user = getUserFromSession(req)
    employee = employeeController.getEmployeeById(int(match.group(1)))
    args = {
        "user": user,
        "employee": employee
    }
    resp.body = template.render(**args)
    resp.send(sock)

@server.register(["POST"], "/employee/new$")
def routeEmployeeNewPOST(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    template = env.get_template("employeeNewPOST.html")
    user = getUserFromSession(req)
    e = employeeController.createEmployee(fname=req.form.data["fname"].asStr(),
                                          lname=req.form.data["lname"].asStr(),
                                          admin=req.form.data["admin"].asBool())
    args = {
        "user": user,
        "employee": e
    }
    resp.body = template.render(**args)
    resp.send(sock)

@server.register(["GET"], "/employee/new$")
def routeEmployeeNewGET(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    template = env.get_template("employeeNewGET.html")
    user = getUserFromSession(req)
    args = {
        "user": user
    }
    resp.body = template.render(**args)
    resp.send(sock)

@server.register(["GET"], "/employee/list$|/employee/list\?(\&?(pg|pgSize)=([0-9]+))(\&?(pg|pgSize)=([0-9]+))")
def routeEmployeeList(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    template = env.get_template("employeeList.html")
    pg = 1
    pgSize = 20
    if match.group(2) == "pg":
        pg = int(match.group(3))
        pgSize = int(match.group(6))
    elif match.group(2) == "pgSize":
        pg = int(match.group(6))
        pgSize = int(match.group(3))
    employees = employeeController.getEmployeeList(offset=(pg-1)*pgSize,count=pgSize)
    user = getUserFromSession(req)
    resp.body = template.render(**args)
    ##todo: finish
    resp.body = template.render(employees=employees,pg=pg,pgSize=pgSize,displayCount=len(employees),totalEmployees=len(employeeController.employeeDict))
    resp.send(sock)

@server.register(["GET"], "/login/([0-9]+)$")
def routeLogin(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    userid = int(match.group(1))
    authHandler.createSession(userid=userid, resp=resp)
    template = env.get_template("index.html")
    resp.body = template.render()
    resp.send(sock)

@server.register(["GET"], "/logout$")
def routeLogout(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    authHandler.invalidateSession(req=req, resp=resp)
    template = env.get_template("index.html")
    resp.body = template.render()
    resp.send(sock)

@server.register(["GET"],"/api/(xhr|json)/employee/list\?pg=([0-9]+)\&pgSize=([0-9]+)$")
def routeApiEmployeeList(req: httpserver.Request, match: Match, sock: socket):
    resp = httpserver.Response()
    resp.send(sock)

server.start()
server.listenthread.join()