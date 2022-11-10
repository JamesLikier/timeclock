import bootstrap
from jlpyhttp.http import Request, Response, STATUS_CODES
from re import Match
import reloadable
from jlpyhttp.sessionhandler import SessionHandler

rh = bootstrap.ROUTE_HANDLER
jinja = bootstrap.JINJA
ec = bootstrap.EMPLOYEE_CONTROLLER

@rh.register(["GET"],"/punch/new")
def routePunchNewGET(resp: Response, session, **kwargs):
    valid, eid = session
    if valid:
        args = {
            'user': ec.getEmployeeById(eid)
        }
        resp.body = jinja.get_template("punch/punchNewGET.html").render(**args)
    else:
        resp.body = jinja.get_template("user/login_required.html").render()
    resp.send()