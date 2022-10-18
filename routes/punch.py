import settings
from httphelper import Request, Response, STATUS_CODES
from re import Match
import reloadable
from sessionhandler import SessionHandler

rh = settings.ROUTE_HANDLER
jinja = settings.JINJA
ec = settings.EMPLOYEE_CONTROLLER

@rh.register(["GET"],"/punch/new")
def routePunchNewGET(req: Request, match: Match, resp: Response, session, sessionHandler: SessionHandler):
    valid, eid = session
    
    if valid:
        args = {
            'user': ec.getEmployeeById(eid)
        }
        resp.body = jinja.get_template("punch/punchNewGET.html").render(**args)
    else:
        resp.body = jinja.get_template("user/login_required.html").render()
    resp.send()