import logging
import timeclock as tc
import SQLiteControllers as sc
from jlpyutil.SQLiteHelper import SQLRequestQueue
from jlpyutil.cachedfilemanager import CachedFileManager
from jlpyhttp.routehandler import RouteHandler
from jlpyhttp.sessionhandler import SessionHandler
from jinja2 import Environment, select_autoescape, FileSystemLoader
from TimeclockAuthHandler import TimeclockAuthHandler
from config import Config

CONFIG = Config()
CONFIG.load()

logging.basicConfig(filename=CONFIG["log_file"], filemode="w", level=logging.DEBUG)

SRQ = SQLRequestQueue(CONFIG["database"])
SRQ.start()

SALT = None
with open(CONFIG["salt_file"],"rb") as f:
    SALT = f.read()

EMPLOYEE_CONTROLLER: tc.EmployeeController = sc.EmployeeController(SRQ)
PUNCH_CONTROLLER: tc.PunchController = sc.PunchController(
    SRQ, 
    CONFIG["timeclock"]["min_hours_for_break"], 
    CONFIG["timeclock"]["break_minutes"]
    )

CACHE = CachedFileManager()
SESSION_HANDLER = SessionHandler()
AUTH_HANDLER = TimeclockAuthHandler(srq=SRQ, salt=SALT)
ROUTE_HANDLER = RouteHandler(sessionHandler=SESSION_HANDLER,authHandler=AUTH_HANDLER)

JINJA = Environment(
    loader = FileSystemLoader(CONFIG["jinja"]["template_folder"]),
    autoescape = select_autoescape()
)
JINJA.filters["floor"] = lambda val, floor: val if val > floor else floor
JINJA.filters["ceil"] = lambda val, ceil: val if val < ceil else ceil
