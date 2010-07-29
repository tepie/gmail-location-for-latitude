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
import settings
import time

logging.basicConfig(level=logging.DEBUG)

def get_location_from_inbox():
  http_gmail = oauth_wrap.get_wrapped_http(file=settings.FILENAME_GMAIL_TOKEN_JSON)
  
  parameters = {}
  resp, content = http_gmail.request(uritemplate.expand(settings.GMAIL_ATOM_ENDPOINT,parameters))
  
  if resp['status'] != '200': raise Exception('Invalid response %s.' % resp['status'])
  
  d = feedparser.parse(content)
  
  result = {}
  
  regex = re.compile(settings.LOCATION_REGEX_PREFIX)
  
  for entry in d.entries:
  	if entry.author_detail.email == settings.TRUSTED_FROM_EMAIL:
  		match_obj = regex.match(entry.summary)
  		if match_obj != None:
  			logging.debug("found matching email location to set, email summary: %s" % entry.summary)
  			result['timestampMs'] = time.mktime(entry.published_parsed) 
  			result['location'] = entry.summary[match_obj.end():] 
  			return result
  
  logging.warning("no location text found in atom feed")
  
  return None

def geocode_loc_text(loc_text):
  encoded_text = urllib.quote(loc_text)
  endpoint = settings.GEOCODDE_ENDPOINT % (encoded_text)
  
  logging.debug('geocode request endpoint: %s' % endpoint)
  
  f = urllib2.urlopen(endpoint)
  json_obj = simplejson.load(f)
  lat_lng_map = json_obj['results'][0]['geometry']['location']
  
  logging.debug('geocode result map: %s' % lat_lng_map)
  
  return lat_lng_map

def get_stamp_from_location(current_loc_json):
	json_obj = simplejson.loads(current_loc_json)	
	return json_obj["data"]["timestampMs"]

def main():
  #http://www.google.com/url?sa=D&q=http://www.googleapis.com/discovery/0.1/describe%3Fapi%3Dlatitude%26apiVersion%3D1%26pp%3D1&usg=AFQjCNGSM47dMOefinzyE7Cqa0lmx7tqsA
  http = oauth_wrap.get_wrapped_http(file=settings.FILENAME_LAT_TOKEN_JSON)
  
  http_url= settings.LATITUDE_ENDPONT % ('currentLocation')
  parameters={'granularity': 'best'}
  resp, content = http.request(uritemplate.expand(http_url, parameters))
  
  if resp['status'] != '200': raise Exception('Invalid response %s.' % resp['status'])
  
  curr_location_stamp = get_stamp_from_location(content)
  
  logging.debug('current location timestamp: %s' % curr_location_stamp)
  
  loc_inbox = get_location_from_inbox()
  
  logging.debug('location from inbox: %s' % loc_inbox)
  
  if loc_inbox == None:
  	logging.warning('no location update found in inbox, value is %s' % loc_inbox)
  	
  elif curr_location_stamp > loc_inbox['timestampMs']:
  	logging.warning('current location is more recent than the inbox value, will not update: %s > %s == True' % (curr_location_stamp,loc_inbox['timestampMs']))
  	
  else:
  	geo_map = geocode_loc_text(loc['location'])
  		
  	parameters={"data":{"kind":"latitude#location","latitude":geo_map['lat'],"longitude":geo_map['lng'],"accuracy":130,"altitude":35}}
  	
  	logging.debug('update location parameters: %s' % parameters)
  	
  	resp, content = http.request(http_url,'POST',
  	  body=simplejson.dumps(parameters),
  	  headers = {'Content-type': 'application/json'})
  	
  	if resp['status'] != '200': raise Exception('Invalid response %s.' % resp['status'])
  	
  	logging.debug('updated location response: %s' % content)
 
if __name__ == '__main__':
  main()
