import numpy as np
import time
import datetime
import socket
import matplotlib
matplotlib.use('Agg')
from PIL import Image
from flask import Flask, send_file
import psycopg2

import matplotlib.pyplot as plt

app = Flask(__name__)


##for database collection
conn = psycopg2.connect(
	database = "data1", user='amanda', password='temppwd', host='127.0.0.1', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()


xData=[]
yData=[]

HOST = 'localhost'
PORT = 12345

count =0
#while True:
while count<20:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		try:
			s.connect((HOST, PORT))
			data = s.recv(1024)
			print("Tempterature received: " , data.decode())
			print("\n")

			x = datetime.datetime.now()
			y = int(data.decode()) 

			xData.append(x)
			yData.append(y)

			##INSERTING data into database
			cursor.execute('''INSERT INTO  temp(VAL, TIME) VALUES(%s, %s);''', (y, x))

			conn.commit()
			print("data inserted...........")
            # plt.plot(x, y)
		#plt.gcf().autofmt_xdate()
			count+=1
		except ConnectionRefusedError as e:
			print(f"Connection refused: {e}")
			time.sleep(1)
			continue

	time.sleep(0.5)

conn.close()
#plt.plot(xData, yData)
#plt.gcf().autofmt_xdate()
#print("saving plot")
#plt.savefig('tempChart.png')

plt.plot(xData, yData, marker='o', linestyle='-', color='b', label='Temperature')
plt.title('Temperature Plot')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("temp.png")
plt.show()


plt.close()
#@app.route('/192.168.7.2/plot')
#def serve_plot():
#	return send_file('tempChart.png', mimetype='image/png')


#if __name__ == '__main__':
#	app.run(debug=True)

#plot it in a chart
#send chart to web server

