# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import oauth_wrap
import uritemplate
import feedparser
import re, urllib,urllib2,simplejson
import logging

logging.basicConfig(level=logging.DEBUG)

TRUSTED_FROM_EMAIL='4403764038@vtext.com'
LOCATION_REGEX_PREFIX = "^[Ll][Oo][Cc]\s"
GMAIL_ATOM_ENDPOINT = 'https://mail.google.com/mail/feed/atom/'
GEOCODDE_ENDPOINT = 'http://maps.google.com/maps/api/geocode/json?address=%s&sensor=false'
LATITUDE_ENDPONT = 'https://www.googleapis.com/latitude/v1/%s'

OAUTH_GMAIL_DATA_FILE = 'oauth_token_gmail.dat'
OAUTH_LATITUDE_DATA_FILE = 'oauth_token.dat'

def get_location_from_inbox():
  http_gmail = oauth_wrap.get_wrapped_http(file=OAUTH_GMAIL_DATA_FILE)
  
  parameters = {}
  resp, content = http_gmail.request(uritemplate.expand(GMAIL_ATOM_ENDPOINT,parameters))
  
  logging.debug('gmail request response: %s' % resp)
  
  d = feedparser.parse(content)
  
  regex = re.compile(LOCATION_REGEX_PREFIX)
  
  for entry in d.entries:
  	if entry.author_detail.email == TRUSTED_FROM_EMAIL:
  		match_obj = regex.match(entry.summary)
  		if match_obj != None:
  			logging.debug("found matching email location to set, email summary: %s" % entry.summary)
  			return entry.summary[match_obj.end():]
  
  logging.warning("no location text found in atom feed")
  
  return None

def geocode_loc_text(loc_text):
  encoded_text = urllib.quote(loc_text)
  endpoint = GEOCODDE_ENDPOINT % (encoded_text)
  
  logging.debug('geocode request endpoint: %s' % endpoint)
  
  f = urllib2.urlopen(endpoint)
  json_obj = simplejson.load(f)
  lat_lng_map = json_obj['results'][0]['geometry']['location']
  
  logging.debug('geocode result map: %s' % lat_lng_map)
  
  return lat_lng_map

def main():
  #http://www.google.com/url?sa=D&q=http://www.googleapis.com/discovery/0.1/describe%3Fapi%3Dlatitude%26apiVersion%3D1%26pp%3D1&usg=AFQjCNGSM47dMOefinzyE7Cqa0lmx7tqsA
  http = oauth_wrap.get_wrapped_http(file=OAUTH_LATITUDE_DATA_FILE)
  
  http_url= LATITUDE_ENDPONT % ('currentLocation')
  parameters={'granularity': 'best'}
  resp, content = http.request(uritemplate.expand(http_url, parameters))
  
  logging.debug('current location response: %s' % resp)
  
  loc = get_location_from_inbox()
  
  logging.debug('location from inbox: %s' % loc)
  
  if loc == None:
  	logging.warning('no location update found in inbox, value is %s' % loc)
  else:
  	geo_map = geocode_loc_text(loc)
  		
  	parameters={"data":{"kind":"latitude#location","latitude":geo_map['lat'],"longitude":geo_map['lng'],"accuracy":130,"altitude":35}}
  	
  	logging.debug('update location parameters: %s' % parameters)
  	
  	resp, content = http.request(http_url,'POST',
  	  body=simplejson.dumps(parameters),
  	  headers = {'Content-type': 'application/json'})
  	
  	logging.debug('updated location response: %s' % resp)
  
if __name__ == '__main__':
  main()
