

# IP Store

web server to use like a dynamic dns, but more primitive


## installing

```
pyvenv env
source env/bin/activate
pip install -U -r pip_requirements.txt
```


## running

1. edit config.py (see comments and examples in file for options)
2. `python app.py`


## using

- GET /hostname?token=mytoken --> ip address or error (retrieves ip for hostname - if no hostname, returns client ip)

- POST /hostname?token=mytoken --> ip address or error (saves/updates client's ip to hostname)

- DELETE /hostname?token=mytoken --> ok or error (deletes the hostname entry)

### example

- cronjob on server to call `curl -X POST "https://example.com/home?token=abcdef"` every hour or so.

- client-side uses something like `IP=$(curl "https://example.com/home?token=abcdef") # now do something with $IP`

This way it works kind of like a pseudo dynamic dns service.

## License

TODO

Copyright © 2016 Samuel Walladge
