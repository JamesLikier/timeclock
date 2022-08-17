from lib.httpserver import httpserver,httprequest,httpresponse,statuscodes
import time
from socket import socket
import FileBasedControllers as fbc
import lib.timeclock as tc
from re import Match

server = httpserver("10.0.0.100",80)
employeeController: tc.EmployeeController = fbc.FileBasedEmployeeController("employeefile")
punchController: tc.PunchController = fbc.FileBasedPunchController("punchfile")

def timeclock404(req: httprequest, match: Match, sock: socket):
    with open('index.html','rb') as index:
        resp = httpresponse(statuscodes.NOT_FOUND)
        resp.body = index.read().replace(b'@placeholder',b'<h1 id="notfound404">404 - Not Found</h1>')
        resp.send(sock)
server.handler404 = timeclock404

@server.registerstatic("/static/.*")
def routeStatic(req: httprequest, match: Match, sock: socket):
    with open(f"./{req.uri}", 'rb') as f:
        resp = httpresponse(statuscodes.OK)
        resp.body = f.read()
        resp.send(sock)

@server.register(("GET",),"/$")
def routeRoot(req: httprequest, match: Match, sock: socket):
    with open('index.html','rb') as f:
        resp = httpresponse(statuscodes.OK)
        resp.body = f.read().replace(b'@placeholder',b'')
        resp.send(sock)

@server.register(("GET","POST"),"/employee/new$")
def routeRoot(req: httprequest, match: Match, sock: socket):
    with open('index.html','rb') as index:
        with open('templates/employee_new.html','rb') as template:
            templateData = template.read()
            resp = httpresponse(statuscodes.OK)
            resp.body = index.read().replace(b'@placeholder',templateData)
            resp.send(sock)

server.start()
while(True):
    time.sleep(1)