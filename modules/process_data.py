import os
import psycopg2
from datetime import datetime
from pytz import timezone

import modules.arrivals as arrivals

# print("ARE WE GOING OR WHAT")

# stopnum =  "999"
# arrival_id = 1509831815
# route_number =  13
# direction = "Eastbound"
# estimated = 1
# canceled = "0"
# arrival_estimated = "2020-02-09 22:08:00"
# arrival_scheduled = "2020-02-09 22:04:00"

# arrival_dict = {}
# arrival_dict["1"] = arrivals.Arrival(stopnum, arrival_id, route_number, direction, canceled, estimated, arrival_estimated, arrival_scheduled)

# arrival_dict["1"].arrived = True
# arrival_dict["1"].minutes_off = 4
# arrival_dict["1"].added = False

def update_arrivals_db(arrival_dict):

	#create ssl files
	ssl_cert_path = "client-cert.pem"
	ssl_key_path = "client-key.pem"
	ssl_root_cert_path = "server-ca.pem"

	if not os.path.exists(ssl_cert_path):
		with open(ssl_cert_path, 'w+') as f:
			f.write(os.environ["SSL_CERT"])

		with open(ssl_key_path, 'w+') as f:
			f.write(os.environ["SSL_KEY"])

		with open(ssl_root_cert_path, 'w+') as f:
			f.write(os.environ["SSL_ROOT_CERT"])

	conn = psycopg2.connect(database=str(os.environ["DB_NAME"]),
							user=str(os.environ["DB_USERNAME"]),
							password=str(os.environ["DB_PASSWORD"]),
							host=str(os.environ["DB_HOSTNAME"]),
							port=str(os.environ["DB_PORT"]),
							sslcert=ssl_cert_path,
							sslmode=str(os.environ["SSL_MODE"]),
							sslrootcert=ssl_root_cert_path,
							sslkey=ssl_key_path)
	c = conn.cursor()

	c.execute("""CREATE TABLE IF NOT EXISTS arrivals(insertDate TEXT, 
													 lastUpdated TEXT, 
													 stopNumber TEXT, 
													 route TEXT,
													 direction TEXT,
													 canceled TEXT,
													 minsOff REAL)""")

	today_date = datetime.now(timezone('US/Hawaii')).date().strftime("%m-%d-%Y")\

	for k, v in arrival_dict.items():
		 if arrivals.estimated_and_scheduled_time_unavailable(v):
		 	print("did not add to db")
		 else:
		 	last_updated = datetime.now(timezone('US/Hawaii')).strftime("%m/%d/%Y %I:%M:%S")

		 	params = (today_date, last_updated, v.stop_number, v.route_number, v.direction, v.canceled, v.minutes_off)
		 	query = ("""INSERT INTO arrivals (insertDate, lastUpdated, stopNumber, route, direction, canceled, minsOff)
	    				 VALUES (%s, %s, %s , %s, %s, %s, %s)""")

		 	c.execute(query, params)
		 	conn.commit()
	conn.close()

# update_arrivals_db(arrival_dict)
