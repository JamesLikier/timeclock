from lib.httpserver import httpserver,httprequest,httpresponse,statuscodes
import time
from socket import socket
import FileBasedControllers as fbc
import lib.timeclock as tc
from re import Match
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from lib.cachedfilemanager import CachedFileManager

server = httpserver("10.0.0.100",80)
employeeController: tc.EmployeeController = fbc.FileBasedEmployeeController("employeefile")
punchController: tc.PunchController = fbc.FileBasedPunchController("punchfile")
cache = CachedFileManager()

env = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)

def timeclock404(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    resp.send(sock)

server.handler404 = timeclock404

@server.registerstatic("/static/(.*)$")
def routeStatic(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    f = cache.get(match.group(1))
    if f != None:
        resp.body = f
    else:
        try:
            with open(f"./{req.uri}", 'rb') as f:
                resp.body = f.read()
        except Exception:
            resp.statuscode = statuscodes.NOT_FOUND
        
    resp.send(sock)

@server.register(("GET",),"/$")
def routeRoot(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    template = env.get_template("index.html")
    resp.body = template.render()
    resp.send(sock)

@server.register(("GET",), "/employee/([0-9]+)$")
def routeEmployee(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    template = env.get_template("employee.html")
    employee = employeeController.getEmployeeById(int(match.group(1)))
    resp.body = template.render(employee=employee)
    resp.send(sock)

@server.register(("GET",), "/employee/list$|/employee/list\?pg\=([0-9]+)\&pgSize\=([0-9]+)$")
def routeEmployeeList(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    template = env.get_template("employeeList.html")
    pg = 1 if match.group(1) == None else int(match.group(1))
    pgSize = 10 if match.group(2) == None else int(match.group(2))
    employees = employeeController.getEmployeeList(offset=(pg-1)*pgSize,count=pgSize)
    resp.body = template.render(employees=employees,pg=pg,pgSize=pgSize,displayCount=len(employees))
    resp.send(sock)

@server.register(("GET",),"/api/(xhr|json)/employee/list\?pg=([0-9]+)\&pgSize=([0-9]+)$")
def routeApiEmployeeList(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    resp.send(sock)

server.start()
while(True):
    time.sleep(1)