from email import message
import settings
from jlpyhttp.httphelper import Request, Response, STATUS_CODES
from re import Match
import reloadable
from routes.api.util import Message
import json
from jlpyhttp.sessionhandler import SessionHandler

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA

@rh.register(["GET"], "/api/comp/login")
def loginForm(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    
    msg = Message()
    msg.action = "comp/login"
    msg.result = Message.SUCCESS
    msg.body = jinja.get_template("user/loginForm.html").render()
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/login")
def login(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    
    msg = Message()
    msg.action = "login"
    try:
        data = json.loads(req.body)
        username = data["username"]
        password = data["password"]
        valid = sessionHandler.authUser(username,password,resp)
        if valid:
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
def logout(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    
    sessionHandler.invalidateSession(req=req, resp=resp)
    msg = Message(result=Message.SUCCESS, action="logout")
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"], "/api/setpassword")
def setPassword(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    msg = Message()
    msg.action = "setpassword"
    try:
        data = json.loads(req.body)
        username = data["username"]
        password = data["password"]
        sessionHandler.setPassword(username,password)
        msg.result = msg.SUCCESS
    except Exception:
        msg.result = msg.FAIL
    resp.body = msg.toJSON()
    resp.send()