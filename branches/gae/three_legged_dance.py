# This is sample client three legged oauth dance sample
# from python-oauth2, but modified to work with gmail and latitude.

import urlparse
import oauth2 as oauth
#import httplib2
import urllib
import simplejson
import logging
import settings


try:
    from urlparse import parse_qs, parse_qsl
except ImportError:
    from cgi import parse_qs, parse_qsl

def step1_get_request_token(client,request_token_url):
	# Step 1: Get a request token. This is a temporary token that is used for
	# having the user authorize an access token and to sign the request to obtain
	# said access token.
	
	resp, content = client.request(request_token_url, 'POST', headers=settings.HEADERS,
    	body=urllib.urlencode(settings.PARAMETERS, True))
   
	if resp['status'] != '200': raise Exception('Invalid response %s.' % resp['status'])
  
	request_token = dict(parse_qsl(content))
	
	return request_token

def step2_redirect_to_provider(request_token, authorize_url):

	base_url = urlparse.urlparse(authorize_url)
	query = parse_qs(base_url.query)
	query['oauth_token'] = request_token['oauth_token']

	url = (base_url.scheme, base_url.netloc, base_url.path, base_url.params,urllib.urlencode(query, True), base_url.fragment)
          
	authorize_url = urlparse.urlunparse(url)
	
	return authorize_url

def step3_sign_request(client,oauth_verifier,request_token):
	# Step 3: Once the consumer has redirected the user back to the oauth_callback
	# URL you can request the access token the user has approved. You use the
	# request token to sign this request. After this is done you throw away the
	# request token and use the access token returned. You should store this
	# access token somewhere safe, like a database, for future use.
	token = oauth.Token(request_token['oauth_token'],
		request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)
	
	resp, content = client.request(settings.ACCESS_TOKEN_URL, 'POST', headers=settings.HEADERS,
		body=urllib.urlencode(settings.PARAMETERS, True))
	access_token = dict(parse_qsl(content))
	
	return access_token

def write_access_token_to_file(filename,d):
	f = open(filename, 'w')
	f.write(simplejson.dumps(d))
	f.close()

if __name__ == '__main__':
	consumer = oauth.Consumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
	client = oauth.Client(consumer)
	
	token_lat = step1_get_request_token(client,settings.REQUEST_TOKEN_URL_LAT)
	token_gmail = step1_get_request_token(client,settings.REQUEST_TOKEN_URL_GMAIL)
	
	auth_url_lat = step2_redirect_to_provider(token_lat,settings.AUTHORIZE_URL_LAT)
	auth_url_gmail = step2_redirect_to_provider(token_gmail,settings.AUTHORIZE_URL_GMAIL)
	
	print
	print 'visit the following URLs in your browser and copy the PIN per site'
	print
	print 'google latitude: %s ' % auth_url_lat
	print
	print 'gmail: %s ' % auth_url_gmail
	print
	
	accepted = 'n'
	while accepted.lower() == 'n':
		accepted = raw_input('Have you authorized me? (y/n) ')
	
	oauth_verifier_lat = raw_input('What is the PIN? (latitude) ')
	oauth_verifier_gmail = raw_input('What is the PIN? (gmail) ')

	access_token_lat = step3_sign_request(client,oauth_verifier_lat,token_lat)
	access_token_gmail = step3_sign_request(client,oauth_verifier_gmail,token_gmail)
	
	d = dict(
  		consumer_key = settings.CONSUMER_KEY,
  		consumer_secret = settings.CONSUMER_SECRET)
	
	d.update(access_token_gmail)
	
	write_access_token_to_file(settings.FILENAME_GMAIL_TOKEN_JSON,d)
	
	print
	print 'wrote gmail access token to file: %s' % settings.FILENAME_GMAIL_TOKEN_JSON
	
	d = dict(
  		consumer_key = settings.CONSUMER_KEY,
  		consumer_secret = settings.CONSUMER_SECRET)
	
	d.update(access_token_lat)
	
	write_access_token_to_file(settings.FILENAME_LAT_TOKEN_JSON,d)
	
	print
	print 'wrote latitude access token to file: %s' % settings.FILENAME_LAT_TOKEN_JSON
	