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
        resp = httpresponse()
        resp.body = index.read().replace(b'@placeholder',b'<h1 class="message">404 - Not Found</h1>')
        resp.send(sock)
server.handler404 = timeclock404

@server.registerstatic("/static/.*")
def routeStatic(req: httprequest, match: Match, sock: socket):
    with open(f"./{req.uri}", 'rb') as f:
        resp = httpresponse()
        resp.body = f.read()
        resp.send(sock)

@server.register(("GET",),"/$")
def routeRoot(req: httprequest, match: Match, sock: socket):
    with open('index.html','rb') as f:
        resp = httpresponse()
        resp.body = f.read().replace(b'@placeholder',b'')
        resp.send(sock)

@server.register(("GET","POST"),"/employee/new$")
def routeEmployeeNew(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
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

@server.register(("GET",),"/employee/([0-9]+)$")
def routeEmployee(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    with open('index.html','rb') as indexFile:
        indexTemplate = indexFile.read()
        try:
            e = employeeController.getEmployeeById(int(match.group(1)))
            with open('templates/employee.html','rb') as employeeFile:
                employeeTemplate = employeeFile.read()
                body = employeeTemplate.replace(b'@employeename',f'{e.lname}, {e.fname}'.encode())
                body = indexTemplate.replace(b'@placeholder',body)
                resp.body = body
        except tc.EmployeeNotFound:
            resp.body = indexTemplate.replace(b'@placeholder',b'<div class="message">Employee Not Found</div>')
    resp.send(sock)

@server.register(("GET",),"/employee/list$")
def routeEmployeeList(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    with open('index.html','rb') as indexFile:
        indexTemplate = indexFile.read()
        with open('templates/employee_list.html','rb') as listFile:
            listTemplate = listFile.read()
            with open('templates/employee_listitem.html','rb') as itemFile:
                itemTemplate = itemFile.read()
                items = []
                rowAlt = True
                for e in employeeController.getEmployeeList():
                    rowclass = b'r1' if rowAlt else b'r2'
                    rowAlt = not rowAlt
                    i = itemTemplate.replace(b'@rowclass',rowclass)
                    i = i.replace(b'@employeeid',str(e.id).encode())
                    i = i.replace(b'@employeename',f'{e.lname}, {e.fname}'.encode())
                    items.append(i)
                list = b''.join(items)
                body = indexTemplate.replace(b'@placeholder',listTemplate.replace(b'@employeelist',list))
                resp.body = body
    resp.send(sock)

server.start()
while(True):
    time.sleep(1)