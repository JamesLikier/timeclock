import jinja2
import timeclock as tc
import SQLiteControllers as sc
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
TIMECLOCK_DBFILE = "timeclock.db"

logging.info('Config Settings:')
logging.info(f'{SERVER_ADDR=}')
logging.info(f'{SERVER_PORT=}')
logging.info(f'{EMPLOYEE_FILE=}')
logging.info(f'{PUNCH_FILE=}')

SRQ = sc.SQLRequestQueue(TIMECLOCK_DBFILE)
SRQ.start()
EMPLOYEE_CONTROLLER: tc.EmployeeController = sc.EmployeeController(SRQ)
PUNCH_CONTROLLER: tc.PunchController = sc.PunchController(SRQ)
CACHE = CachedFileManager()
ROUTE_HANDLER = RouteHandler()
SESSION_HANDLER = SessionHandler()

JINJA = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
JINJA.filters["floor"] = lambda val, floor: val if val > floor else floor
JINJA.filters["ceil"] = lambda val, ceil: val if val < ceil else ceil
