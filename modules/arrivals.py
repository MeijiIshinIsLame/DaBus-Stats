import requests
import os
import time
from lxml import etree
from datetime import datetime

import modules.helpers as helpers

API_KEY = str(os.environ.get("BUS_API_KEY"))

class Arrival:

	stop_number = ""
	arrival_id = ""
	route_number = ""
	direction = ""
	estimated = 0
	canceled = 0
	arrival_estimated = ""
	arrival_scheduled = ""
	arrived = False
	minutes_off = 0

	def __init__(self, _stop_number, _arrival_id, _route_number,_direction, _canceled, _estimated, _arrival_estimated, _arrival_scheduled):
		self.stop_number = str(_stop_number)
		self.arrival_id = str(_arrival_id)
		self.route_number = str(_route_number)
		self.direction = str(_direction)
		self.canceled = str(_canceled)
		self.estimated = str(_estimated)
		self.arrival_estimated = _arrival_estimated
		self.arrival_scheduled = _arrival_scheduled

	def update_from(self, updated_arrival):
		self.estimated = updated_arrival.estimated
		self.canceled = updated_arrival.canceled

		if self.arrival_scheduled == "":
			self.arrival_scheduled = updated_arrival.arrival_scheduled

		if self.arrival_estimated != updated_arrival.arrival_estimated:
			self.arrival_estimated = updated_arrival.arrival_estimated

	def pretty_print(self):
		print("\n--Arrival--\n")
		print("stop_number: ", self.stop_number)
		print("arrival_id: ", self.arrival_id)
		print("route_number: ", self.route_number)
		print("direction ", self.direction)
		print("estimated: ", self.estimated)
		print("arrival_estimated: ", self.arrival_estimated)
		print("arrival_scheduled: ", self.arrival_scheduled)
		print("arrived: ", self.arrived)
		print("minutes_off: ", self.minutes_off)
		print("canceled: ", self.canceled)


def get_arrival_list(stopnum):
	arrival_list = {}

	url = (f"http://api.thebus.org/arrivals/?key={API_KEY}&stop={stopnum}")
	response = requests.get(url)
	dom = etree.fromstring(response.content)

	arrivals = dom.findall('arrival')

	for item in arrivals:
		arrival_id = item.find('id').text
		route_number = item.find('route').text
		direction = item.find('direction').text
		estimated = item.find('estimated').text
		canceled = item.find('canceled').text
		date = item.find('date').text
		arrival_estimated = ""
		arrival_scheduled = ""

		#i know, this is stupid...but their estimated returns as 2 sometimes okay.
		if estimated is "1":
			arrival_estimated = date + " " + item.find('stopTime').text
			arrival_estimated = datetime.strptime(arrival_estimated, "%m/%d/%Y %I:%M %p")
		else:
			arrival_scheduled = date + " " + item.find('stopTime').text
			arrival_scheduled = datetime.strptime(arrival_scheduled, "%m/%d/%Y %I:%M %p")

		#create new arrival, and add to dictionary with arrival_id as the key
		new_arrival = Arrival(stopnum, arrival_id, route_number, direction, canceled, estimated, arrival_estimated, arrival_scheduled)
		arrival_list[new_arrival.arrival_id] = new_arrival

	return arrival_list
	

def update_arrivals(old_arrival_list, stopnum):
	print(API_KEY)
	new_arrival_list = get_arrival_list(stopnum)
	popped_arrivals = {}

	for k, v in old_arrival_list.items():
		if k in new_arrival_list:
			v.update_from(new_arrival_list[k])
		else:
			popped_arrivals[k] = v
	
	for k, v in popped_arrivals.items():
		v.arrived = 1
		del old_arrival_list[k]

	final_arrival_list = helpers.merge_dictionaries(old_arrival_list, new_arrival_list)
	return final_arrival_list, popped_arrivals

def finalize_popped_arrivals(arrival_list):
	for k, v in arrival_list.items():
		if v.arrived == True:
			if estimated_and_scheduled_time_unavailable(v):
				print("cannot calculate because of missing values")
			else:
				v.minutes_off = helpers.calculate_minutes_off(v.arrival_estimated, v.arrival_scheduled)
	return arrival_list

#there's gotta be a better way to do this
def estimated_and_scheduled_time_unavailable(arrival):
	return ((arrival.arrival_scheduled == "") or (arrival.arrival_estimated == ""))