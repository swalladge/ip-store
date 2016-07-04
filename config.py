

# set which origins are allowed to access with CORS
cors_origin = "*"

# file to store ip address information for persistance
data_file = 'host_ips.dat'

# interval in seconds to save database to disc
save_interval = 60 * 5  # (5 minutes)

# run tornado server in debug mode or not
debug = False

# auth token
# warning: whitespace is stripped from ends of token in queryparams by server,
# so don't have trailing/leading whitespace in token below
token = "abc"

# whether to enforce token auth or not
needs_auth = True

# tokens that can be used on any hostname request
global_tokens = ['abc', 'def']

# tokens specific to certain hostname - use for in security if you don't trust
# something
tokens = {
        'home': ['abcdef']
}
