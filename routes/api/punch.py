import re
import settings
import reloadable
from httphelper import Request, Response, STATUS_CODES, CONTENT_TYPES
from re import Match
from socket import socket
from timeclock import PunchController, Punch, EmployeeController, Employee
import json
from routes.api.util import Message
import datetime as dt

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
session = settings.SESSION_HANDLER
pc = settings.PUNCH_CONTROLLER
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["POST"],"/api/punch/new")
def punchNew(req: Request, match: Match, sock: socket):
    msg = Message()
    msg.action = "punch/new"
    try:
        date = dt.date.fromisoformat(req.form.get("date",dt.date.today().isoformat()))
        time = dt.time.fromisoformat(req.form.get("time",dt.datetime.now().time().isoformat()))
        datetime = dt.datetime.combine(date,time)
        e = ec.getEmployeeById(req.form["employeeid"].asInt())
        pc.createPunch(e.id,datetime)
        msg.result = Message.SUCCESS
    except Exception:
        msg.result = Message.FAIL
    resp = Response()
    resp.body = msg.toJSON()
    resp.send(sock)

@rh.register(["POST"],"/api/punchclock")
def punchclock(req: Request, match: Match, sock: socket):
    msg = Message()
    msg.action = "punchclock"
    try:
        e = ec.getEmployeeById(req.form["employeeid"].asInt())
        pc.createPunch(e.id)
        msg.result = Message.SUCCESS
        msg.body = f"Punch Accepted: {e.lname}, {e.fname}"
    except Exception:
        msg.result = Message.FAIL
        msg.body = "Invalid Employee ID or PIN"
    resp = Response()
    resp.body = msg.toJSON()
    resp.send(sock)