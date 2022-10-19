import settings
import jlpyhttp.httpserver as httpserver
import routes

server = httpserver.Server(settings.SERVER_ADDR, settings.SERVER_PORT, settings.ROUTE_HANDLER)
server.start()