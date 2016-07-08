#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main application file

import tornado.ioloop
from tornado.web import Application, url
import tornado.httpserver
import json
import importlib
import tornado.options
import logging

import config as cfg
from basehanders import ApiHandler

log = logging.getLogger("tornado.general")


class MainHandler(ApiHandler):
    """handles stuff"""

    def get(self, host=None):
        """returns the ip address"""

        ip = None
        # returns ip of request if no host specified
        if host is None:
            if self.current_user in cfg.global_tokens or \
                    self.current_user in cfg.read_index_tokens or \
                    not cfg.read_index_requires_auth:
                self.write(json.dumps(self.db.dump(), indent=2))
            else:
                return self.send_error(401,
                                       reason='invalid or missing token in params')
        else:
            if (cfg.tokens.get(host, None) and
                    self.current_user in cfg.tokens[host]) or \
                    self.current_user in cfg.global_tokens or \
                    self.current_user in cfg.read_tokens or \
                    not cfg.read_requires_auth:
                ip = self.db.get(host)
                if ip:
                    self.write(ip)
                else:
                    self.send_error(404, reason='host not found')
            else:
                return self.send_error(401,
                                       reason='invalid or missing token in params')

    def post(self, host=None):
        """create data entry with ip address of host"""
        if host is None:
            return self.send_error(400, reason='no host specified')
        else:
            if (cfg.tokens.get(host, None) and
                    self.current_user in cfg.tokens[host]) or \
                    self.current_user in cfg.global_tokens:
                ip = self.request.headers.get('X-Real-Ip', None)
                if ip is None:
                    ip = self.request.remote_ip
                res = self.db.put(host, ip)

                # all good
                if res >= 200 and res < 300:
                    return self.write(ip)
                # uh oh
                else:
                    return self.send_error(res, reason='failed to update the dns')
            else:
                return self.send_error(401,
                                       reason='invalid or missing token in params')

    def delete(self, host=None):
        """delete a data entry"""
        if host is not None:
            if (cfg.tokens.get(host, None) and
                    self.current_user in cfg.tokens[host]) or \
                    self.current_user in cfg.global_tokens:
                res = self.db.delete(host)
                if not res:
                    return self.send_error(404, reason='host did not exist')
            else:
                return self.send_error(401,
                                       reason='invalid or missing token in params')
        else:
            return self.send_error(400, reason='host must be specified')


class Database():
    def __init__(self, data_file, backend=None):
        self.datafile = data_file
        self.backend = backend
        self.data = {}

    def init(self):
        try:
            with open(self.datafile) as f:
                self.data = json.load(f)
        except:
            log.info('error reading file - attempting to create first')
            self.save()

    def save(self):
        # dump the dictionary json-encoded to the savefile
        # not that important, since it's for dynamic ip addresses
        with open(self.datafile, 'w') as f:
            json.dump(self.data, f)

    def get(self, host):
        return self.data.get(host, None)

    def delete(self, host):
        ip = self.data.pop(host, None)
        self.save()
        return ip

    def put(self, host, ip):
        old = self.data.get(host, None)
        self.data[host] = ip
        status = 200
        if old != ip:
            if self.backend:
                status = self.backend.update(host, ip)
                if status >= 200 and status < 300:
                    self.save()
            else:
                self.save()
        return status

    def dump(self):
        return self.data


def main():
    tornado.options.parse_command_line()

    backend = None
    if cfg.dns_backend:
        backend_module = importlib.import_module('dns_backends.{}'.format(cfg.dns_backend))
        backend = backend_module.DynDNS()

    db = Database(cfg.data_file, backend)
    db.init()

    app = Application([
        url(r'^//?$', MainHandler),
        url(r'^/([^/]+)/?$', MainHandler),
        ],
        debug=cfg.debug,
        db=db
    )

    app.listen(cfg.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
