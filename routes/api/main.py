import sys
import bootstrap
import reloadable
from jlpyhttp.http import Request, Response
import json
from routes.api.util import Message
import datetime as dt
import logging

rh = bootstrap.ROUTE_HANDLER
jinja = bootstrap.JINJA

@rh.register(["GET"], "/api/main")
def main(resp: Response, **kwargs):
    resp.body = jinja.get_template("api/main.html").render()
    resp.send()