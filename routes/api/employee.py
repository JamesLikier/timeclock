import bootstrap
from jlpyhttp.http import Request, Response, STATUS_CODES
from re import Match
import json
import reloadable
from routes.api.util import Message
from jlpyhttp.sessionhandler import SessionHandler

rh = bootstrap.ROUTE_HANDLER
jinja = bootstrap.JINJA
ec = bootstrap.EMPLOYEE_CONTROLLER

def newEmployee(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs) -> None:
    respData = dict()
    respData["action"] = "employee/new"
    try:
        data = json.loads(req.body)
        employee = ec.createEmployee(
            username = data["username"],
            fname = data["fname"],
            lname = data["lname"],
            admin = data.get("admin",False)
        )
        respData["success"] = True
        respData["text"] = f"Successfully created employee: {lname}, {fname}."
    except Exception:
        respData["success"] = False
        respData["text"] = "An error occurred while creating new employee."
    resp.body = json.dumps(respData)
    resp.send()

def updateEmployee(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs) -> None:
    pass

def deleteEmployee(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs) -> None:
    pass

def getEmployee(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs) -> None:
    pass

def getEmployeeList(req: Request, resp: Response, sessionHandler: SessionHandler, **kwargs) -> None:
    pass