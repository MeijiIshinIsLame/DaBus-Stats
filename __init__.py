import time
import random
from os import system
import _thread
from datetime import datetime

import modules.arrivals as arrivals
import modules.stops as stops
import modules.helpers as helpers
import modules.process_data as db

#change to stopnum
def track_data(stopnum):
	arrival_list = arrivals.get_arrival_list(stopnum)
	print(arrival_list)

	i = 0

	for k, v in arrival_list.items():
		i += 1

	print("Tracking for:", stopnum, "arrivals: ", i, "\n----------------------\n\n")

	while True:
		#kill thread when 2 AM is hit
		if helpers.restart_time_hit():
			time.sleep(120)
			print("Thread restarted!")
			return ""

		next_arrival_list, popped_arrivals = arrivals.update_arrivals(arrival_list, stopnum)

		time.sleep(20)

		for k, v in next_arrival_list.items():
			print("\nStop: ", v.stop_number)
			break

		if popped_arrivals:
			print("\npopped arrivals\n")
			for k, v in popped_arrivals.items():
				v.pretty_print()

			print("----------------------")

		if popped_arrivals: 
			popped_arrivals = arrivals.finalize_popped_arrivals(popped_arrivals)
			db.update_arrivals_db(popped_arrivals)
			popped_arrivals = {}

def make_stop_list(numstops):
	stops_to_track = []
	total_stops_file = 'stops.txt'
	skip_file = 'stops_completed.txt'

	stop_list = list(open(total_stops_file))
	stops_to_skip = list(open(skip_file))

	if len(stops_to_skip) == len(stop_list):
		helpers.clear_text_file(skip_file)
		stops_to_skip = list(open(skip_file))

	for i in range(numstops):
		random_stop_number = random.choice(stop_list)

		if not stops_to_skip:
			stops_to_track.append(random_stop_number)
		else:
			while random_stop_number in stops_to_skip:
				random_stop_number = random.choice(stop_list)
			stops_to_track.append(random_stop_number)

		with open(skip_file, "a") as file:
				file.write(str(random_stop_number))

		stops_to_skip = list(open(skip_file))

	return stops_to_track

if __name__ == "__main__":
	numstops = 45
	stops_to_track  = make_stop_list(numstops)

	for stop in stops_to_track:
		_thread.start_new_thread(track_data, (stop, ))
		time.sleep(3)

	while True:
		if helpers.restart_time_hit():
			stops_to_track = make_stop_list(numstops)
			print("\n\nrestarting......\n\n")

			time.sleep(120)

			#Threads are killed when they return a value
			#hence why I don't need to kill the already existing threads, because they return at restart time.
			for stop in stops_to_track:
				_thread.start_new_thread(track_data, (stop, ))
				time.sleep(3)
