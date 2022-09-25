import settings
import lib.httpserver as httpserver
from routes import main, static, employee

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT)

server.start()
server.listenthread.join()