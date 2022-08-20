from lib.httpserver import httpserver,httprequest,httpresponse,statuscodes
import time
from socket import socket
import FileBasedControllers as fbc
import lib.timeclock as tc
from re import Match
from lib.cachedfilemanager import CachedFileManager

server = httpserver("10.0.0.100",80)
employeeController: tc.EmployeeController = fbc.FileBasedEmployeeController("employeefile")
punchController: tc.PunchController = fbc.FileBasedPunchController("punchfile")
templateCache: CachedFileManager = CachedFileManager(basedir="./templates")

def timeclock404(req: httprequest, match: Match, sock: socket):
    marker = b'placeholder'
    msg = b'<h1 class="message">404 - Not Found</h1>'
    resp = httpresponse()
    resp.body = templateCache["index.html"].replace(marker,msg)
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
    marker = b'@placeholder'
    msg = b''
    resp = httpresponse()
    resp.body = templateCache["index.html"].replace(marker,msg)
    resp.send(sock)

@server.register(("GET","POST"),"/employee/new$")
def routeEmployeeNew(req: httprequest, match: Match, sock: socket):
    marker = b'@placeholder'
    indexTemplate = templateCache["index.html"]
    resp = httpresponse()
    if req.method == "GET":
        employeeNewTemplate = templateCache["employee_new.html"]
        resp.body = indexTemplate.replace(marker,employeeNewTemplate)
    elif req.method == "POST":
        e = employeeController.createEmployee(fname=req.form.data["fname"].value,lname=req.form.data["lname"].value,admin=req.form.data.get("admin","")=="True")
        msg = f'<div class="message">Created New Employee: <a href="/employee/{e.id}">{e.lname}, {e.fname}</a></div>'.encode()
        resp.body = indexTemplate.replace(marker,msg)
    resp.send(sock)

@server.register(("GET",),"/employee/([0-9]+)$")
def routeEmployee(req: httprequest, match: Match, sock: socket):
    indexTemplate = templateCache["index.html"]
    indexMarker = b'@placeholder'
    resp = httpresponse()
    try:
        e = employeeController.getEmployeeById(int(match.group(1)))
        employeeTemplate = templateCache["employee.html"]
        employeeMarker = b'@employeename'
        body = employeeTemplate.replace(employeeMarker,f'{e.lname}, {e.fname}'.encode())
        body = indexTemplate.replace(indexMarker,body)
        resp.body = body
    except tc.EmployeeNotFound:
        msg = b'<div class="message">Employee Not Found</div>'
        resp.body = indexTemplate.replace(indexMarker,msg)
    resp.send(sock)

@server.register(("GET",),"/employee/list$")
def routeEmployeeList(req: httprequest, match: Match, sock: socket):
    resp = httpresponse()
    indexTemplate = templateCache["index.html"]
    empListTemplate = templateCache["employee_list.html"]
    empListItemTemplate = templateCache["employee_listitem.html"]

    items = []
    rowAlt = True
    for e in employeeController.getEmployeeList():
        rowclass = b'r1' if rowAlt else b'r2'
        rowAlt = not rowAlt
        i = empListItemTemplate.replace(b'@rowclass',rowclass)
        i = i.replace(b'@employeeid',str(e.id).encode())
        i = i.replace(b'@employeename',f'{e.lname}, {e.fname}'.encode())
        items.append(i)
    list = b''.join(items)
    body = empListTemplate.replace(b'@employeelist',list)
    body = indexTemplate.replace(b'@placeholder',body)
    resp.body = body
    resp.send(sock)

server.start()
while(True):
    time.sleep(1)