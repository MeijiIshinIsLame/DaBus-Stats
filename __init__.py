import time
from datetime import datetime

import modules.arrivals as arrivals
import modules.stops as stops
import modules.helpers as helpers
import modules.process_data as db

if __name__ == "__main__":

	arrival_list = arrivals.get_arrival_list(999)
	print(arrival_list)
	print("original arrival list\n")

	for k, v in arrival_list.items():
		v.pretty_print()

	print("----------------------")

	while True:
		next_arrival_list, popped_arrivals = arrivals.update_arrivals(arrival_list, 999)

		time.sleep(10)

		print("popped arrivals\n")

		for k, v in popped_arrivals.items():
			v.pretty_print()

		print("----------------------")

		if popped_arrivals: 
			popped_arrivals = arrivals.finalize_popped_arrivals(popped_arrivals)
			db.update_arrivals_db(popped_arrivals)
			popped_arrivals = {}
			print("Popped arrivals added\n")
		else:
			print("No popped arrivals\n")