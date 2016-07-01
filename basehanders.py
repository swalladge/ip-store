# These inherit from RequestHander and should be inherited by specific route
# handlers. They provide authentication methods and such.

from tornado.web import RequestHandler

import config as cfg


class BaseHandler(RequestHandler):

    def initialize(self):
        self.db = self.settings.get('db')
        self.user = None

    def send_data(self, data):
        """writes the json data with status message (basic wrapper)"""
        self.write({
            'success': True,
            'status': 200,
            'data': data
            });

    def write_error(self, status, reason=None, data=None):
        body = {'status': status,
                'success': False}
        if reason:
            body['reason'] = reason
        if data:
            body['data'] = data
        self.write(body)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", cfg.cors_origin)


class ApiHandler(BaseHandler):
    """base handler for all api handlers
       handles authentication, returns errors, etc."""

    # also sets current_user
    def prepare(self):

        token = self.get_query_argument('token', None)
        if token == cfg.token:
            self.current_user = True
        else:
            self.current_user = False
            if cfg.needs_auth:
                return self.send_error(401, reason='auth required - invalid or missing token in params')
