import jinja2
import timeclock as tc
import FileBasedControllers as fbc
from  cachedfilemanager import CachedFileManager
from routehandler import RouteHandler
from sessionhandler import SessionHandler
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import logging
import time

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

#create default admin employee for testing
if len(EMPLOYEE_CONTROLLER.employeeDict) == 0:
    EMPLOYEE_CONTROLLER.createEmployee("ADMIN","ADMIN",True)