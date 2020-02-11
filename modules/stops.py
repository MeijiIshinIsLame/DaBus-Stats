import requests

def get_stop_list():
	last_checked = get_last_stop()

	print("lastline: ", last_checked)

	for i in range(last_checked, 7000):
		try:
			response = requests.get(f"http://api.thebus.org/arrivals/?key={API_KEY}&stop={i}", timeout=10)
		except:
			response = requests.get(f"http://api.thebus.org/arrivals/?key={API_KEY}&stop={i}", timeout=10)

		time.sleep(0.5)

		if "<arrival>" in response.text:
			with open("stops.txt", "a") as file:
				file.write(str(i) + "\n")
			print(f"{i} returned response!")
			print(response)
		else:
			print(f"{i} no response")
			print(response)

def get_last_stop():
	last_checked = 0

	with open('stops.txt', 'r') as file:
		lines = file.read().splitlines()
		last_line = lines[-1]
		if last_line is '':
			last_line = lines[-2]
		last_checked = int(last_line)

	return last_checked + 1

def get_stops_total():
	return sum(1 for line in open('stops.txt'))