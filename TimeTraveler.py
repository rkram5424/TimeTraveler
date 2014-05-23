#!/usr/bin/env python2

# Another ryBorg project.
# I SHOULD be working on Senior Design.

# Description:
# Tired of having to remember to change your computer's timezone
# every time you cross the border? Well with this handy-dandy tool,
# you are reminded once you connect to the internet if there is a 
# timezone mismatch between your computer and current ISP.

# BUGS/ERRORS
# Only Linux Support
# No automation yet. Script must be run manually.

# Requirements:
# Python 2.7
# The ability an know-how to run this script at runtime.

import urllib, urllib2, time, os, sys, platform
from geopy import geocoders

class TimeTraveler:
	IP_WEBSITE = 'http://www.whatismyip.com/'
	
	def __init__(self):
		while not(self.check_connection()):
			time.sleep(10)
		ip = self.get_ip()
		city = (self.get_city())
		print('Your current city: %s' % city)
		coords = self.get_coords(city)
		print('%s\'s coordinates: %s' % (city, coords))
		ip_timezone = self.get_timezone(coords)
		print('Your current timezone: %s' % ip_timezone)
		sys_timezone = (int(time.timezone/60/60))
		print('Your computer\'s timezone: %s' % sys_timezone)
		
		tz_mismatch = False
		if(str(sys_timezone) != str(ip_timezone)):
			tz_mismatch = True
			
		if tz_mismatch:
			if platform.system() == 'Windows':
				pass
			elif platform.system() == 'darwin':
				pass
			else:
				gmt_offset = 'GMT' + ip_timezone
				print('Timezone Missmatch Detected')
				correct_prompt = raw_input('Would you like to correct the timezone? [Y/n]: ')
				if correct_prompt == 'Y' or correct_prompt == 'y':
					print('Your password is required to complete this operation.')
					os.system('sudo ln -sf /usr/share/zoneinfo/Etc/'+ gmt_offset + ' /etc/localtime')
					print('All done! Have a nice day!')
				else:
					print('Nothing changed! Have a nice day!')
		else: 
			print('No mismatch. \nYour system is set to your current timezone.\nHave a nice day!')

	def get_ip(self):
		return urllib.urlopen('http://ip.42.pl/raw').read()

	def get_city(self):
		city = ''
		response = urllib.urlopen(self.IP_WEBSITE)
		page_source = response.read()
		city += self.find_between(page_source, 'City:</td><td>', '</td>')
		city += ', '
		city += self.find_between(page_source, 'State/Region:</td><td>', '</td>')
		return city
		
	def get_coords(self, city):
		g = geocoders.GoogleV3()
		place, (lat, lng) = g.geocode(city)
		lat = '%.5f' % lat
		lng = '%.5f' % lng
		coord_array = [lat, lng]
		return coord_array

	def get_timezone(self, coords):
		response = urllib.urlopen('http://www.earthtools.org/timezone/' + str(coords[0]) + '/' + str(coords[1]))
		page_source = response.read()
		tz_offset = self.find_between(page_source, '<offset>', '</offset>')
		return tz_offset

	def check_connection(self):
		try:
			response=urllib2.urlopen('http://74.125.228.100', timeout=1)
			return True
		except urllib2.URLError as err: pass
		return False

	def find_between(self, s, first, last):
		try:
			start = s.index(first) + len(first)
			end = s.index( last, start )
			return s[start:end]
		except ValueError:
			return ""

if __name__ == '__main__':
	TimeTraveler()
