from re import Match
import sys
import settings
import reloadable
from jlpyhttp.http import Request, Response, STATUS_CODES, CONTENT_TYPES
from timeclock import PunchController, Punch, EmployeeController, Employee
import timeclock
import json
from routes.api.util import Message
import datetime as dt
from jlpyhttp.sessionhandler import SessionHandler
import logging

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
pc = settings.PUNCH_CONTROLLER
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["POST"],"/api/punch/new")
def punchNew(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    msg = Message()
    msg.action = "punch/new"
    try:
        data = json.loads(req.body)
        date = dt.date.fromisoformat(data['date'])
        time = dt.time.fromisoformat(data['time'])
        datetime = dt.datetime.combine(date,time)
        e = ec.getEmployeeById(int(data["employeeid"]))
        pc.createPunch(e.id,datetime)
        msg.result = Message.SUCCESS
    except Exception:
        msg.result = Message.FAIL
    
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/punch/delete")
def punchDelete(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    msg = Message()
    msg.action = "punch/delete"
    try:
        data = json.loads(req.body)
        pc.deletePunchById(int(data['pid']))
        msg.result = Message.SUCCESS
    except Exception:
        msg.result = Message.FAIL
    
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/punch/list")
def punchList(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    msg = Message()
    msg.action = "punch/list"
    try:
        msg.result = Message.SUCCESS
        data = json.loads(req.body)
        logging.debug(data)
        employeeid = int(data["employeeId"])
        startDate = dt.date.fromisoformat(data["startDate"])
        endDate = dt.date.fromisoformat(data["endDate"])
        pairList = pc.getPunchPairsByEmployeeId(employeeid,startDate,endDate,True)
        template = jinja.get_template("api/punch/punchlist.html")
        msg.body = template.render(startDate=startDate,endDate=endDate,employeeid=employeeid,pairList=pairList)
    except Exception:
        logging.error(sys.exc_info())
        msg.result = Message.FAIL
    
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/punchclock")
def punchclock(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    msg = Message()
    msg.action = "punchclock"
    try:
        data = json.loads(req.body)
        employeeid = int(data['employeeid'])
        e = ec.getEmployeeById(employeeid)
        pc.createPunch(e.id)
        msg.result = Message.SUCCESS
        msg.body = f"Punch Accepted: {e.lname}, {e.fname}"
    except Exception:
        msg.result = Message.FAIL
        msg.body = "Invalid Employee ID or PIN"
    
    resp.body = msg.toJSON()
    resp.send()