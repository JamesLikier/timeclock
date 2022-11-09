import timeclock as tc
import SQLiteControllers as sc
from jlpyutil.SQLiteHelper import SQLRequestQueue
from jlpyutil.cachedfilemanager import CachedFileManager
from jlpyhttp.routehandler import RouteHandler
from jlpyhttp.sessionhandler import SessionHandler
from jinja2 import Environment, select_autoescape, FileSystemLoader
import logging
from TimeclockAuthHandler import TimeclockAuthHandler

logging.basicConfig(filename="timeclock.log", filemode="w", level=logging.DEBUG)

SERVER_ADDR = '10.0.0.100'
SERVER_PORT = 80
EMPLOYEE_FILE = 'employeefile'
PUNCH_FILE = 'punchfile'
TIMECLOCK_DBFILE = "timeclock.db"
SALT_FILE = "salt"
MIN_HOURS_FOR_BREAK = 7.0
BREAK_MINUTES = 30.0

logging.info('Config Settings:')
logging.info(f'{SERVER_ADDR=}')
logging.info(f'{SERVER_PORT=}')
logging.info(f'{EMPLOYEE_FILE=}')
logging.info(f'{PUNCH_FILE=}')

SALT = None
with open(SALT_FILE,"rb") as f:
    SALT = f.read()

SRQ = SQLRequestQueue(TIMECLOCK_DBFILE)
SRQ.start()
EMPLOYEE_CONTROLLER: tc.EmployeeController = sc.EmployeeController(SRQ)
PUNCH_CONTROLLER: tc.PunchController = sc.PunchController(SRQ, MIN_HOURS_FOR_BREAK, BREAK_MINUTES)
CACHE = CachedFileManager()
SESSION_HANDLER = SessionHandler()
AUTH_HANDLER = TimeclockAuthHandler(srq=SRQ, salt=SALT)
ROUTE_HANDLER = RouteHandler(sessionHandler=SESSION_HANDLER,authHandler=AUTH_HANDLER)

JINJA = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
JINJA.filters["floor"] = lambda val, floor: val if val > floor else floor
JINJA.filters["ceil"] = lambda val, ceil: val if val < ceil else ceil
