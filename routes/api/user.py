import re
import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
from socket import socket
import json

rh = settings.ROUTE_HANDLER
session = settings.SESSION_HANDLER
jinja = settings.JINJA

@rh.register(["GET"], "/api/login")
def loginForm(req: Request, match: Match, sock: socket):
    resp = Response()
    resp.body = jinja.get_template("loginForm.html").render()
    resp.send(sock)

@rh.register(["POST"],"/api/login")
def login(req: Request, match: Match, sock: socket):
    username = req.form["username"].asStr()
    password = req.form["password"].asStr()
    userid = int(username)
    resp = Response()
    session.createSession(userid=userid,resp=resp)
    data = {
        "result": "success",
        "formName": req.form["formName"]
    }
    resp.body = json.dumps(data)
    resp.send(sock)

@rh.register(["POST"], "/api/logout")
def logout(req: Request, match: Match, sock: socket):
    resp = Response()
    session.invalidateSession(req=req,resp=resp)
    data = {
        "result": "success",
        "formName": req.form["formName"]
    }
    resp.body = json.dumps(data)
    resp.send(sock)