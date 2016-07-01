#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main application file

import tornado.ioloop
from tornado.web import Application, url
from tornado.escape import json_decode
import tornado.httpserver
import json

import config as cfg
from basehanders import ApiHandler
import utils


class MainHandler(ApiHandler):
    """handles stuff"""

    def get(self, host=None):
        """returns the ip address"""
        use_json = self.get_query_argument('json', None)

        ip = None
        if host is None:
            ip = self.request.remote_ip
        else:
            ip = self.db.get(host)

        if use_json:
            if ip:
                self.send_data({'ip': ip})
            else:
                self.send_error(404, reason='host not found')
        else:
            if ip:
                self.write(ip)
            else:
                # TODO: non-json error
                self.send_error(404, reason='host not found')

    def _update_or_add(self, host=None):
        use_json = self.get_query_argument('json', None)
        if host is None:
            return self.send_error(400, reason='no host specified')
        else:
            # TODO: check if ip address specified in post/put data body
            ip = self.request.remote_ip
            self.db.put(host, ip)

            # TODO: use use_json
            return self.send_data({'ip': ip})

    def post(self, host=None):
        """create data entry with ip address of host"""
        return self._update_or_add(host)

    def put(self, host=None):
        """update a data entry"""
        return self._update_or_add(host)

    def delete(self, host=None):
        """delete a data entry"""
        use_json = self.get_query_argument('json', None)
        if host is not None:
            res = self.db.delete(host)
            # if res, return success, else return 404
        # TODO: use use_json
        return self.send_data(None)



class Database():
    def __init__(self, data_file):
        self.datafile = data_file
        self.data = {}

    def init(self):
        try:
            with open(self.datafile) as f:
                self.data = json.load(f)
        except:
            print('error reading file - attempting to create first')
            self.save()

    def save(self):
        with open(self.datafile, 'w') as f:
            json.dump(self.data, f)

    def get(self, host):
        return self.data.get(host, None)

    def delete(self, host):
        ip = self.data.pop(host, None)
        self.save()
        return ip

    def put(self, host, ip):
        self.data[host] = ip
        self.save()
        return ip


def main():
    db = Database(cfg.data_file)
    db.init()

    app = Application([
        url(r'^//?$', MainHandler),
        url(r'^/([^/]+)/?$', MainHandler),
        ],
        debug=cfg.debug,
        db=db
    )

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
