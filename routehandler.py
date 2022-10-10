import re
from socket import socket
from httphelper import Request, Response, STATUS_CODES
import logging

class RouteHandler():
    def __init__(self):
        self.handlers = dict()
        self.statichandlers = dict()
        self.handler404 = None

    @staticmethod
    def default404(req: Request, match: re.Match, sock: socket):
        resp = Response(sock=sock)
        resp.statuscode = STATUS_CODES[404]
        resp.send()

    def register(self, methods: list, uriRegex: str):
        logging.info(f'Registering: {uriRegex=} {methods=}')
        def inner(func):
            for method in methods:
                if method not in self.handlers:
                    self.handlers[method] = dict()
                self.handlers[method][re.compile(uriRegex)] = func
            return func
        return inner

    def registerstatic(self, uriRegex: str):
        logging.info(f'Registering Static: {uriRegex=}')
        def inner(func):
            self.statichandlers[re.compile(uriRegex)] = func
            return func
        return inner

    def register404(self, func):
        logging.info('Registering: 404')
        self.handler404 = func
        return func

    def dispatch(self, req: Request, sock: socket):
        logging.info(f'Received Request: {req.uri} {req.method}')
        handler = None
        m = None
        if req.method in self.handlers:
            for uriRegex in self.handlers[req.method].keys():
                uriRegex: re.Pattern
                m = uriRegex.match(req.uri)
                if m is not None:
                    handler = self.handlers[req.method][uriRegex]
                    break
        if handler is None:
            for uriRegex in self.statichandlers.keys():
                uriRegex: re.Pattern
                m = uriRegex.match(req.uri)
                if m is not None:
                    handler = self.statichandlers[uriRegex]
                    break
        if handler is None:
            logging.info(f'Could not find handler for: {req.uri} {req.method}')
        else:
            logging.info(f'Dispatching handler for: {req.uri} {req.method}')
        handler = handler or self.handler404 or RouteHandler.default404
        handler(req, m, sock)