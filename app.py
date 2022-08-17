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
    resp = httpresponse(statuscodes.OK)
    with open('index.html','rb') as index:
        if req.method == "GET":
            with open('templates/employee_new.html','rb') as template:
                templateData = template.read()
                resp.body = index.read().replace(b'@placeholder',templateData)
        elif req.method == "POST":
            e = employeeController.createEmployee(fname=req.form.data["fname"].value,lname=req.form.data["lname"].value,admin=req.form.data.get("admin","")=="True")
            data = f'<div class="message">Created New Employee: <a href="/employee/{e.id}">{e.lname}, {e.fname}</a></div>'.encode()
            resp.body = index.read().replace(b'@placeholder',data)
    resp.send(sock)

server.start()
while(True):
    time.sleep(1)