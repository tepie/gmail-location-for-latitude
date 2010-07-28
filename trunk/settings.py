__version__ = '0.1'

HEADERS = {
    'user-agent': 'gmail-location-for-latitude/%s' % __version__,
    'content-type': 'application/x-www-form-urlencoded'
    }

CONSUMER_KEY = 'gmail-location-for-latitude.appspot.com'
CONSUMER_SECRET = 'cflcYnKXy0Hj/97TpaF9VA4U'

REQUEST_TOKEN_URL_LAT = 'https://www.google.com/accounts/OAuthGetRequestToken?domain=gmail-location-for-latitude.appspot.com&scope=https://www.googleapis.com/auth/latitude'
AUTHORIZE_URL_LAT = 'https://www.google.com/latitude/apps/OAuthAuthorizeToken?domain=gmail-location-for-latitude.appspot.com&scope=https://www.googleapis.com/auth/latitude'
ACCESS_TOKEN_URL = 'https://www.google.com/accounts/OAuthGetAccessToken'

REQUEST_TOKEN_URL_GMAIL = 'https://www.google.com/accounts/OAuthGetRequestToken?domain=gmail-location-for-latitude.appspot.com&scope=https://mail.google.com/mail/feed/atom/'
AUTHORIZE_URL_GMAIL = 'https://www.google.com/accounts/OAuthAuthorizeToken?domain=gmail-location-for-latitude.appspot.com&scope=https://mail.google.com/mail/feed/atom/'

PARAMETERS = {
	  'xoauth_displayname': 'gmail-location-for-latitude',
	  'oauth_callback': 'oob'
		}
		
FILENAME_GMAIL_TOKEN_JSON = 'oauth_token_gmail.dat'
FILENAME_LAT_TOKEN_JSON = 'oauth_token_lat.dat'