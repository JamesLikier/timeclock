import settings
import httpserver as httpserver
from routes import main, static, employee

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT, settings.ROUTE_HANDLER)

server.start()
server.listenthread.join()