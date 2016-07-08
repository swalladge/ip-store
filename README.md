# IP Store

web server to use like a dynamic dns, but more primitive


## Features

- light and easy to setup
- maintains small dictionary of host/ip mappings, with save-to-disk for backup
- able to use apis like Digitalocean's through plugins for real dynamic dns


## Installing

Requires python3.

```
pyvenv env
source env/bin/activate
pip install -r requirements.txt
```


## Running

1. edit config.py (see comments and examples in file for options)
2. `python app.py`

You can also pass any tornado options on the commandline (like `python app.py --log-file-prefix=thefile.log`).


## Using

- GET /?token=mytoken --> json object of all hosts - formatted as `{"host":"ip address"}`

- GET /hostname?token=mytoken --> ip address or error (retrieves ip for hostname - if no hostname, returns client ip)

- POST /hostname?token=mytoken --> ip address or error (saves/updates client's ip to hostname)

- DELETE /hostname?token=mytoken --> ok or error (deletes the hostname entry)


### Example

- cronjob on server to call `curl -X POST "https://example.com/home?token=abcdef"` every hour or so

- client-side uses something like `IP=$(curl "https://example.com/home?token=abcdef") ; ssh user@$IP`
- if dynamic dns backend configured, you can simply use the `home.myconfigureddomain.tld`, since it will be dynamically
  updated

This way it works as a dynamic dns service.


## License

    IP Store - simple, fast dynamic DNS-like service
    Copyright (C) 2016 Samuel Walladge

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Copyright © 2016 Samuel Walladge
