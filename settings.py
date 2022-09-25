import lib.timeclock as tc
import FileBasedControllers as fbc
from  lib.cachedfilemanager import CachedFileManager
from lib.routehandler import RouteHandler
from lib.sessionhandler import SessionHandler
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import logging

logging.basicConfig(filename="timeclock.log", filemode="w", level=logging.DEBUG)

SERVER_ADDR = '10.0.0.100'
SERVER_PORT = 80
EMPLOYEE_FILE = 'employeefile'
PUNCH_FILE = 'punchfile'

EMPLOYEE_CONTROLLER: tc.EmployeeController = fbc.FileBasedEmployeeController(EMPLOYEE_FILE)
PUNCH_CONTROLLER: tc.PunchController = fbc.FileBasedPunchController(PUNCH_FILE)
CACHE = CachedFileManager()
ROUTE_HANDLER = RouteHandler()
SESSION_HANDLER = SessionHandler()

JINJA = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
JINJA.filters["floor"] = lambda val, floor: val if val > floor else floor
JINJA.filters["ceil"] = lambda val, ceil: val if val < ceil else ceil