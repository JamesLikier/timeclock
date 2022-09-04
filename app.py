from lib.httpserver import httpserver,httprequest,httpresponse,statuscodes
import time
from socket import socket
import FileBasedControllers as fbc
import lib.timeclock as tc
from re import Match
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from lib.cachedfilemanager import CachedFileManager
import logging

server = httpserver("10.0.0.100",80)
employeeController: tc.EmployeeController = fbc.FileBasedEmployeeController("employeefile")
punchController: tc.PunchController = fbc.FileBasedPunchController("punchfile")
cache = CachedFileManager()

logging.basicConfig(filename="timeclock.log", filemode="w", level=logging.DEBUG)

env = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
env.filters["floor"] = lambda val, floor: val if val > floor else floor
env.filters["ceil"] = lambda val, ceil: val if val < ceil else ceil

def timeclock404(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    resp.body = b'404 - Not Found'
    resp.send(sock)

server.handler404 = timeclock404

@server.registerstatic("/static/(.*)$")
def routeStatic(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    urlFilepath = match.group(1)
    paths = tuple(urlFilepath.split("/"))

    f = cache.get(".","static",*paths)
    if f != None:
        resp.body = f
    else:
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

@server.register(("POST",), "/employee/new$")
def routeEmployeeNewPOST(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    e = employeeController.createEmployee(fname=req.form.data["fname"].asStr(),
                                          lname=req.form.data["lname"].asStr(),
                                          admin=req.form.data["admin"].asBool())
    template = env.get_template("employeeNewPOST.html")
    resp.body = template.render(employee=e)
    resp.send(sock)

@server.register(("GET",), "/employee/new$")
def routeEmployeeNewGET(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    template = env.get_template("employeeNewGET.html")
    resp.body = template.render()
    resp.send(sock)

@server.register(("GET",), "/employee/list$|/employee/list\?pg\=([0-9]+)\&pgSize\=([0-9]+)$")
def routeEmployeeList(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    template = env.get_template("employeeList.html")
    pg = 1 if match.group(1) == None else int(match.group(1))
    pgSize = 20 if match.group(2) == None else int(match.group(2))
    employees = employeeController.getEmployeeList(offset=(pg-1)*pgSize,count=pgSize)
    resp.body = template.render(employees=employees,pg=pg,pgSize=pgSize,displayCount=len(employees),totalEmployees=len(employeeController.employeeDict))
    resp.send(sock)

@server.register(("GET",),"/api/(xhr|json)/employee/list\?pg=([0-9]+)\&pgSize=([0-9]+)$")
def routeApiEmployeeList(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    resp.send(sock)

server.start()
while(True):
    time.sleep(1)