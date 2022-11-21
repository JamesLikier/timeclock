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

@rh.register(["GET"], "/api/login")
def loginForm(resp: Response, **kwargs):
    msg = Message()
    msg.success = True
    msg.text = jinja.get_template("api/login.html").render()
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/login")
def login(req: Request, resp: Response, sessionHandler: SessionHandler, authHandler: AuthHandler, **kwargs):
    msg = Message()
    msg.action = "login"
    logging.debug(f'{req.body}')
    try:
        data = json.loads(req.body)
        username = data["username"]
        password = data["password"]
        logging.debug(f'{username=} and {password=}')
        valid, eid = authHandler.validateAuth(username,password)
        if valid:
            sessionHandler.createSession(userid=eid,resp=resp)
            msg.success = True
            msg.text = "Login Successful"
        else:
            msg.success = False
            msg.text = "Invalid Username or Password"
    except Exception:
        msg.success = False
        msg.text = "Error during login."
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["GET"], "/api/logout")
def logout(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs):
    sessionHandler.invalidateSession(req=req, resp=resp)
    msg = Message(success=True, action="logout")
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
        msg.success = True
    except Exception:
        msg.success = False
    resp.body = msg.toJSON()
    resp.send()