Fetches your location from GMail and updates your location on Latitude.

Stolen from the following:

http://code.google.com/p/gdata-python-client/source/browse/v3/

Re-worked example to work with Latitude and GMail.

Main concept is to manage your location with simple text messaging via Google APIs.

Currently a command line tool per the example, but will be moving to the App Engine.

The following is the flow:

  1. Setup OAuth tokens for access to GMail and Latitude
  1. Gmail inbox access will read data via Atom feed for location string
  1. Current location is accessed from Latitude
  1. If the inbox location time is more recent then the current location time, then lets update it
  1. Location string is then geocoded from your inbox
  1. Location is updated with lat / lng from the inbox text

Done. You can then schedule the run program to loop and continue to check your inbox for updates.