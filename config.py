

# set which origins are allowed to access with CORS
cors_origin = "*"

# file to store ip address information for persistance
data_file = 'host_ips.dat'

# run tornado server in debug mode or not
debug = False

# auth token
# warning: whitespace is stripped from ends of token in queryparams by server,
# so don't have trailing/leading whitespace in token below
token = "abc"

# whether to enforce token auth or not
needs_auth = True
