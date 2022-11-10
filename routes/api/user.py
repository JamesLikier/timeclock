import logging
import bootstrap
from jlpyhttp.http import Request, Response, STATUS_CODES
from re import Match
import reloadable
from routes.api.util import Message
import json
from jlpyhttp.sessionhandler import SessionHandler
from jlpyhttp.authhandler import AuthHandler

rh = bootstrap.ROUTE_HANDLER
jinja = bootstrap.JINJA

@rh.register(["GET"], "/api/comp/login")
def loginForm(resp: Response, **kwargs):
    msg = Message()
    msg.action = "comp/login"
    msg.result = Message.SUCCESS
    msg.body = jinja.get_template("user/loginForm.html").render()
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/login")
def login(req: Request, resp: Response, sessionHandler: SessionHandler, authHandler: AuthHandler, **kwargs):
    msg = Message()
    msg.action = "login"
    try:
        data = json.loads(req.body)
        username = data["username"]
        password = data["password"]
        valid, eid = authHandler.validateAuth(username,password)
        if valid:
            sessionHandler.createSession(userid=eid,resp=resp)
            msg.result = Message.SUCCESS
            msg.body = "Login Successful"
        else:
            msg.result = Message.FAIL
            msg.body = "Invalid Username or Password"
    except Exception:
        msg.result = Message.FAIL
        msg.body = "Invalid Username or Password"
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["GET"], "/api/logout")
def logout(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs):
    sessionHandler.invalidateSession(req=req, resp=resp)
    msg = Message(result=Message.SUCCESS, action="logout")
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"], "/api/setpassword")
def setPassword(req: Request, resp: Response, sessionHandler: SessionHandler, authHandler: AuthHandler, **kwargs):
    msg = Message()
    msg.action = "setpassword"
    try:
        data = json.loads(req.body)
        username = data["username"]
        password = data["password"]
        currentPassword = data["currentPassword"]
        valid, eid = authHandler.validateAuth(username, currentPassword)
        if valid:
            authHandler.setPassword(username,password)
        else:
            raise Exception
        msg.result = msg.SUCCESS
    except Exception:
        msg.result = msg.FAIL
    resp.body = msg.toJSON()
    resp.send()