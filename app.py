import bootstrap
from bootstrap import CONFIG
import jlpyhttp.httpserver as httpserver
import routes

server = httpserver.Server(CONFIG["server"]["addr"], CONFIG["server"]["port"], bootstrap.ROUTE_HANDLER)
server.start()