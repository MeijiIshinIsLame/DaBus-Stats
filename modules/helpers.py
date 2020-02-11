from datetime import datetime

def merge_dictionaries(dict1, dict2):
	for k, v in dict2.items():
		if k in dict1:
			pass
		else:
			dict1[k] = v
	return dict1

def calculate_minutes_off(estimated_time, schedule_time):
	time_off = estimated_time - schedule_time
	mins_off = time_off.total_seconds() / 60
	return mins_off

#est = datetime.strptime("2/10/2020 12:13 AM", "%m/%d/%Y %I:%M %p")
#sce = datetime.strptime("2/9/2020 11:59 PM", "%m/%d/%Y %I:%M %p")

#print(calculate_minutes_off(est, sce))