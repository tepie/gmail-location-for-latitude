# This is sample client three legged oauth dance sample
# from python-oauth2, but modified to work with Buzz.

import urlparse
import oauth2 as oauth
import httplib2
import urllib
import simplejson

__version__ = '0.1'

try:
    from urlparse import parse_qs, parse_qsl
except ImportError:
    from cgi import parse_qs, parse_qsl

headers = {
    'user-agent': 'gdata-python-v3-sample-client/%s' % __version__,
    'content-type': 'application/x-www-form-urlencoded'
    }

consumer_key = 'gmail-location-for-latitude.appspot.com'
consumer_secret = 'cflcYnKXy0Hj/97TpaF9VA4U'

request_token_url = 'https://www.google.com/accounts/OAuthGetRequestToken?domain=gmail-location-for-latitude.appspot.com&scope=https://www.googleapis.com/auth/latitude'
authorize_url = 'https://www.google.com/latitude/apps/OAuthAuthorizeToken?domain=gmail-location-for-latitude.appspot.com&scope=https://www.googleapis.com/auth/latitude'
access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'

request_token_url_gmail = 'https://www.google.com/accounts/OAuthGetRequestToken?domain=gmail-location-for-latitude.appspot.com&scope=https://mail.google.com/mail/feed/atom/'
authorize_url_gmail = 'https://www.google.com/accounts/OAuthAuthorizeToken?domain=gmail-location-for-latitude.appspot.com&scope=https://mail.google.com/mail/feed/atom/'

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

# Step 1: Get a request token. This is a temporary token that is used for
# having the user authorize an access token and to sign the request to obtain
# said access token.
parameters = {
  'xoauth_displayname': 'gmail-location-for-latitude',
  'oauth_callback': 'oob'
    }

resp, content = client.request(request_token_url, 'POST', headers=headers,
    body=urllib.urlencode(parameters, True))
    
resp_gmail, content_gmail = client.request(request_token_url_gmail, 'POST', headers=headers,
    body=urllib.urlencode(parameters, True))
    
if resp['status'] != '200':
  print content
  raise Exception('Invalid response %s.' % resp['status'])
  
if resp_gmail['status'] != '200':
  print content
  raise Exception('Invalid response %s.' % resp['status'])

request_token = dict(parse_qsl(content))
request_token_gmail = dict(parse_qsl(content_gmail))

print 'Request Token:'
print '    - oauth_token        = %s' % request_token['oauth_token']
print '    - oauth_token_secret = %s' % request_token['oauth_token_secret']
print
print '    - oauth_token        = %s' % request_token_gmail['oauth_token']
print '    - oauth_token_secret = %s' % request_token_gmail['oauth_token_secret']
print

# Step 2: Redirect to the provider. Since this is a CLI script we do not
# redirect. In a web application you would redirect the user to the URL
# below.

base_url = urlparse.urlparse(authorize_url)
query = parse_qs(base_url.query)
query['oauth_token'] = request_token['oauth_token']

base_url_gmail = urlparse.urlparse(authorize_url_gmail)
query_gmail = parse_qs(base_url_gmail.query)
query_gmail['oauth_token'] = request_token_gmail['oauth_token']

print urllib.urlencode(query, True)
print urllib.urlencode(query_gmail, True)

url = (base_url.scheme, base_url.netloc, base_url.path, base_url.params,
       urllib.urlencode(query, True), base_url.fragment)
       
url_gmail = (base_url_gmail.scheme, base_url_gmail.netloc, base_url_gmail.path, base_url_gmail.params,
       urllib.urlencode(query_gmail, True), base_url_gmail.fragment)
       
authorize_url = urlparse.urlunparse(url)
authorize_url_gmail = urlparse.urlunparse(url_gmail)

print 'Go to the following link in your browser:'
print authorize_url
print
print authorize_url_gmail
print


# After the user has granted access to you, the consumer, the provider will
# redirect you to whatever URL you have told them to redirect to. You can
# usually define this in the oauth_callback argument as well.
accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')
oauth_verifier_gmail = raw_input('What is the PIN? (gmail)')

# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this
# access token somewhere safe, like a database, for future use.
token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

token_gmail = oauth.Token(request_token_gmail['oauth_token'],
    request_token_gmail['oauth_token_secret'])
token_gmail.set_verifier(oauth_verifier_gmail)

client_gmail = oauth.Client(consumer, token_gmail)

resp, content = client.request(access_token_url, 'POST', headers=headers,
    body=urllib.urlencode(parameters, True))
access_token = dict(parse_qsl(content))

print access_token

resp_gmail, content_gmail = client_gmail.request(access_token_url, 'POST', headers=headers,
    body=urllib.urlencode(parameters, True))
access_token_gmail = dict(parse_qsl(content_gmail))

print access_token_gmail

print 'Access Token:'
print '    - oauth_token        = %s' % access_token['oauth_token']
print '    - oauth_token_secret = %s' % access_token['oauth_token_secret']
print
print '    - oauth_token        = %s' % access_token_gmail['oauth_token']
print '    - oauth_token_secret = %s' % access_token_gmail['oauth_token_secret']
print
print 'You may now access protected resources using the access tokens above.'
print

d = dict(
  consumer_key = consumer_key,
  consumer_secret = consumer_secret
    )
d.update(access_token)

f = open('oauth_token.dat', 'w')
f.write(simplejson.dumps(d))
f.close()

d_gmail = dict(
  consumer_key = consumer_key,
  consumer_secret = consumer_secret
    )
d_gmail.update(access_token_gmail)

f = open('oauth_token_gmail.dat', 'w')
f.write(simplejson.dumps(d_gmail	))
f.close()
