# These inherit from RequestHander and should be inherited by specific route
# handlers. They provide authentication methods and such.

from tornado.web import RequestHandler

import config as cfg


class BaseHandler(RequestHandler):

    def initialize(self):
        self.db = self.settings.get('db')
        self.user = None

    def write_error(self, status, reason=None):
        self.write(str(status) + str(': ' + str(reason)) if reason is not None else '')

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", cfg.cors_origin)


class ApiHandler(BaseHandler):
    """base handler for all api handlers
       handles authentication, returns errors, etc."""

    # also sets current_user
    def prepare(self):
        self.current_user = self.get_query_argument('token', None)
