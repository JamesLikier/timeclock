import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
from socket import socket
import reloadable
from routes.api.util import Message

rh = settings.ROUTE_HANDLER
session = settings.SESSION_HANDLER
jinja = settings.JINJA

@rh.register(["GET"], "/api/login")
def loginForm(req: Request, match: Match, sock: socket):
    resp = Response()
    msg = Message(result=Message.SUCCESS, body=jinja.get_template("user/loginForm.html").render())
    resp.body = msg.toJSON()
    resp.send(sock)

@rh.register(["POST"],"/api/login")
def login(req: Request, match: Match, sock: socket):
    resp = Response()
    msg = Message()
    msg.action = "login"
    try:
        username = req.form["username"].asStr()
        password = req.form["password"].asStr()
        userid = int(username)
        session.createSession(userid=userid,resp=resp)
        msg.result = Message.SUCCESS
        msg.body = "Login Successful"
    except Exception:
        msg.result = Message.FAIL
        msg.body = "Invalid Username or Password"
    resp.body = msg.toJSON()
    resp.send(sock)

@rh.register(["POST"], "/api/logout")
def logout(req: Request, match: Match, sock: socket):
    resp = Response()
    session.invalidateSession(req=req,resp=resp)
    msg = Message(result=Message.SUCCESS, action="logout")
    resp.body = msg.toJSON()
    resp.send(sock)