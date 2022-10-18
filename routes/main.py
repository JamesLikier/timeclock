import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
import reloadable
import timeclock as tc
import datetime as dt
from sessionhandler import SessionHandler

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER
pc = settings.PUNCH_CONTROLLER

@rh.register(["GET"],"/$")
def routeRoot(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    
    template = jinja.get_template("index.html")
    startDate = dt.date.today() - dt.timedelta(weeks=2)
    endDate = dt.date.today()
    valid,eid = session
    args = {
        "user": None
    }
    if valid:
        args["user"] = ec.getEmployeeById(eid)
        punchList = pc.getPunchesByEmployeeId(eid,startDate,endDate)
        startState = 'in'
        if len(punchList) > 0:
            startState = pc.getPunchState(punchList[0])
        pairList = tc.paddedPairPunches(punchList, startState, startDate, endDate)
        args["pairList"] = pairList
        args["employeeid"] = eid
        args["startDate"] = startDate
        args["endDate"] = endDate
    resp.body = template.render(**args)
    resp.send()

@rh.register(["GET"], "/logout$")
def routeLogout(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    
    sessionHandler.invalidateSession(req=req, resp=resp)
    template = jinja.get_template("index.html")
    resp.body = template.render()
    resp.send()
