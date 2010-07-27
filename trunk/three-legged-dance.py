# This is sample client three legged oauth dance sample
# from python-oauth2, but modified to work with Buzz.

import urlparse
import oauth2 as oauth
import httplib2
import urllib
import simplejson
import logging

__version__ = '0.1'

try:
    from urlparse import parse_qs, parse_qsl
except ImportError:
    from cgi import parse_qs, parse_qsl

headers = {
    'user-agent': 'gmail-location-for-latitude/%s' % __version__,
    'content-type': 'application/x-www-form-urlencoded'
    }

consumer_key = 'gmail-location-for-latitude.appspot.com'
consumer_secret = 'cflcYnKXy0Hj/97TpaF9VA4U'

request_token_url_lat = 'https://www.google.com/accounts/OAuthGetRequestToken?domain=gmail-location-for-latitude.appspot.com&scope=https://www.googleapis.com/auth/latitude'
authorize_url_lat = 'https://www.google.com/latitude/apps/OAuthAuthorizeToken?domain=gmail-location-for-latitude.appspot.com&scope=https://www.googleapis.com/auth/latitude'
access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'

request_token_url_gmail = 'https://www.google.com/accounts/OAuthGetRequestToken?domain=gmail-location-for-latitude.appspot.com&scope=https://mail.google.com/mail/feed/atom/'
authorize_url_gmail = 'https://www.google.com/accounts/OAuthAuthorizeToken?domain=gmail-location-for-latitude.appspot.com&scope=https://mail.google.com/mail/feed/atom/'

parameters = {
	  'xoauth_displayname': 'gmail-location-for-latitude',
	  'oauth_callback': 'oob'
		}

def step1_get_request_token(client,request_token_url):
	# Step 1: Get a request token. This is a temporary token that is used for
	# having the user authorize an access token and to sign the request to obtain
	# said access token.
	
	resp, content = client.request(request_token_url, 'POST', headers=headers,
    	body=urllib.urlencode(parameters, True))
   
	if resp['status'] != '200':
  		print content
  		raise Exception('Invalid response %s.' % resp['status'])
  
	request_token = dict(parse_qsl(content))
	
	return request_token

def step2_redirect_to_provider(request_token, authorize_url):

	base_url = urlparse.urlparse(authorize_url)
	query = parse_qs(base_url.query)
	query['oauth_token'] = request_token['oauth_token']

	url = (base_url.scheme, base_url.netloc, base_url.path, base_url.params,urllib.urlencode(query, True), base_url.fragment)
          
	authorize_url = urlparse.urlunparse(url)
	
	return authorize_url

def step3_sign_request(client,access_token_url,oauth_verifier,request_token):
	# Step 3: Once the consumer has redirected the user back to the oauth_callback
	# URL you can request the access token the user has approved. You use the
	# request token to sign this request. After this is done you throw away the
	# request token and use the access token returned. You should store this
	# access token somewhere safe, like a database, for future use.
	token = oauth.Token(request_token['oauth_token'],
		request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)
	
	resp, content = client.request(access_token_url, 'POST', headers=headers,
		body=urllib.urlencode(parameters, True))
	access_token = dict(parse_qsl(content))
	
	return access_token

def write_access_token_to_file(filename,d):
	f = open(filename, 'w')
	f.write(simplejson.dumps(d))
	f.close()

if __name__ == '__main__':
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)
	
	token_lat = step1_get_request_token(client,request_token_url_lat)
	token_gmail = step1_get_request_token(client,request_token_url_gmail)
	
	auth_url_lat = step2_redirect_to_provider(token_lat,authorize_url_lat)
	auth_url_gmail = step2_redirect_to_provider(token_gmail,authorize_url_gmail)
	
	print
	print 'visit the following URLs in your browser and copy the PIN per site'
	print
	print 'google latitude: %s' % auth_url_lat
	print
	print 'gmail: %s' % auth_url_gmail
	print
	
	accepted = 'n'
	while accepted.lower() == 'n':
		accepted = raw_input('Have you authorized me? (y/n) ')
	
	oauth_verifier_lat = raw_input('What is the PIN? (latitude)')
	oauth_verifier_gmail = raw_input('What is the PIN? (gmail)')

	access_token_lat = step3_sign_request(client,access_token_url,oauth_verifier_lat,token_lat)
	access_token_gmail = step3_sign_request(client,access_token_url,oauth_verifier_gmail,token_gmail)
	
	d = dict(
  		consumer_key = consumer_key,
  		consumer_secret = consumer_secret)
	
	d.update(access_token_gmail)
	
	write_access_token_to_file('oauth_token_gmail.dat',d)
	
	d = dict(
  		consumer_key = consumer_key,
  		consumer_secret = consumer_secret)
	
	d.update(access_token_lat)
	
	write_access_token_to_file('oauth_token_lat.dat',d)
	