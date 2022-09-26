import settings
import httpserver as httpserver
from routes import main, static, employee
from routes.api import user

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT, settings.ROUTE_HANDLER)

server.start()
server.listenthread.join()