import sys
import bootstrap
import reloadable
from jlpyhttp.http import Request, Response
import json
from routes.api.util import Message
import datetime as dt
import logging

rh = bootstrap.ROUTE_HANDLER
jinja = bootstrap.JINJA
pc = bootstrap.PUNCH_CONTROLLER
ec = bootstrap.EMPLOYEE_CONTROLLER

@rh.register(["POST"],"/api/punch/new")
def punchNew(req: Request, resp: Response, **kwargs):
    msg = Message()
    msg.action = "punch/new"
    try:
        data = json.loads(req.body)
        date = dt.date.fromisoformat(data['date'])
        time = dt.time.fromisoformat(data['time'])
        datetime = dt.datetime.combine(date,time)
        e = ec.getEmployeeById(int(data["employeeid"]))
        pc.createPunch(e.id,datetime)
        msg.success = True
    except Exception:
        msg.success = False
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/punch/delete")
def punchDelete(req: Request, resp: Response, **kwargs):
    msg = Message()
    msg.action = "punch/delete"
    try:
        data = json.loads(req.body)
        pc.deletePunchById(int(data['pid']))
        msg.success = True
    except Exception:
        msg.success = False
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/punch/list")
def punchList(req: Request, resp: Response, **kwargs):
    msg = Message()
    msg.action = "punch/list"
    try:
        msg.success = True
        data = json.loads(req.body)
        logging.debug(data)
        employeeid = int(data["employeeId"])
        startDate = dt.date.fromisoformat(data["startDate"])
        endDate = dt.date.fromisoformat(data["endDate"])
        pairList = pc.getPunchPairsByEmployeeId(employeeid,startDate,endDate,True)
        template = jinja.get_template("api/punch/punchlist.html")
        msg.text = template.render(startDate=startDate,endDate=endDate,employeeid=employeeid,pairList=pairList)
    except Exception:
        logging.error(sys.exc_info())
        msg.success = False
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["POST"],"/api/punchclock")
def punchclock(req: Request, resp: Response, **kwargs):
    msg = Message()
    msg.action = "punchclock"
    try:
        data = json.loads(req.body)
        employeeid = int(data['employeeid'])
        e = ec.getEmployeeById(employeeid)
        pc.createPunch(e.id)
        msg.success = True
        msg.text = f"Punch Accepted: {e.lname}, {e.fname}"
    except Exception:
        msg.success = False
        msg.text = "Invalid Employee ID or PIN"
    resp.body = msg.toJSON()
    resp.send()