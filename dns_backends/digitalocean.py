# module to use DigitalOcean as dynamic dns backend
import requests

import config as cfg


class DynDNS():
    # init is used for everything it needs to setup to be 100% ready
    # use cfg.dns_options for config
    def __init__(self):
        self.token = cfg.dns_options['token']
        self.domain = cfg.dns_options['domain']

        self.headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.token)
        }

        self.hosts = {} # name: id
        url = 'https://api.digitalocean.com/v2/domains/{}/records'.format(self.domain)
        hosts = cfg.dns_options['hosts']
        # load the record ids
        while True:
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            data = res.json()
            records = data['domain_records']
            for record in records:
                if record['name'] in hosts:
                    if record['type'] != 'A':
                        continue
                    id = record['id']
                    self.hosts[record['name']] = id
            url = data['links']['pages'].get('next', None)
            if not url:
                break

        print(self.hosts)

    # called when a host's ip changes
    # - return a http status code
    # - if host not found/allowed, just return 200 and log it
    def update(self, host, ip):
        if host not in self.hosts:
            print('{} not in DNS hosts'.format(host))
            return 200 # unable to update, but don't throw errors (we still use the ip store)

        id = self.hosts[host]
        data = {
                'data': ip
        }
        res = requests.put('https://api.digitalocean.com/v2/domains/{}/records/{}'.format(self.domain, id), headers=self.headers, json=data)
        return res.status_code
