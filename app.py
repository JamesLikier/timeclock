from lib.httpserver import httpserver,httprequest,httpresponse,statuscodes
import time
from socket import socket
import FileBasedControllers as fbc
import lib.timeclock as tc
from re import Match

server = httpserver("localhost",80)
employeeController: tc.EmployeeController = fbc.FileBasedEmployeeController("employeefile")
punchController: tc.PunchController = fbc.FileBasedPunchController("punchfile")

@server.registerstatic("/static/.*")
def routeStatic(req: httprequest, match: Match, sock: socket):
    with open(f"./{req.uri}", 'rb') as f:
        resp = httpresponse(statuscodes.OK)
        resp.body = f.read()
        sock.send(resp.format())

@server.register(("GET",),"/$")
def routeRoot(req: httprequest, match: Match, sock: socket):
    with open('index.html','rb') as f:
        resp = httpresponse(statuscodes.OK)
        resp.body = f.read()
        sock.send(resp.format())

@server.register(("GET",),"/json/punch/id/([0-9]+)$")
def routeGetJSON_punchById(req: httprequest, match: Match, sock: socket):
    resp = httpresponse(statuscodes.OK)
    resp.body = match.group(1).encode()
    sock.send(resp.format())

@server.register(("GET",),"/json/employee/id/([0-9])+$")
def routeGetJSON_employeeById(req: httprequest, match: Match, sock: socket):
    pass

server.start()
while(True):
    time.sleep(1)