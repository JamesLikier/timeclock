from cmath import exp
import settings
from httphelper import Request, Response, STATUS_CODES
from user import User
import re
from socket import socket
import reloadable
import timeclock as tc
import datetime as dt

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
session = settings.SESSION_HANDLER
ec = settings.EMPLOYEE_CONTROLLER
pc = settings.PUNCH_CONTROLLER

@rh.register(["GET"],"/$")
def routeRoot(req: Request, match: re.Match, sock: socket):
    resp = Response()
    user = User.fromSession(req)
    template = jinja.get_template("index.html")
    args = {
        "user": user,
    }
    startDate = dt.date.today() - dt.timedelta(weeks=2)
    endDate = dt.date.today()
    if user is not None:
        punchList = pc.getPunchesByEmployeeId(user.userid,startDate,endDate)
        startState = 'in'
        if len(punchList) > 0:
            startState = pc.getPunchState(punchList[0])
        pairList = tc.paddedPairPunches(punchList, startState, startDate, endDate)
        args["pairList"] = pairList
    resp.body = template.render(**args)
    resp.send(sock)

@rh.register(["GET"], "/login/([0-9]+)$")
def routeLogin(req: Request, match: re.Match, sock: socket):
    resp = Response()
    userid = int(match.group(1))
    user = User.fromUserID(userid)
    if user is not None:
        session.createSession(userid=userid, resp=resp)
    template = jinja.get_template("index.html")
    args = {
        "user": user
    }
    resp.body = template.render(**args)
    resp.send(sock)

@rh.register(["GET"], "/logout$")
def routeLogout(req: Request, match: re.Match, sock: socket):
    resp = Response()
    session.invalidateSession(req=req, resp=resp)
    template = jinja.get_template("index.html")
    resp.body = template.render()
    resp.send(sock)
