import psycopg2
import time
import datetime
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#conn = psycopg2.connect(
#	database = "data1", user='amanda', password='temppwd', host='127.0.0.1', port='5432'
#)
conn = psycopg2.connect(
	database = "testing", user='postgres', password='temppwd', host='localhost', port='5432'
)


conn.autocommit = True
cursor = conn.cursor()

count = 0

xData=[]
yData=[]

while(count<50):
	y = datetime.datetime.now()
	x = random.randint(0, 100)
	cursor.execute('''INSERT INTO numbers(VAL, TIME) VALUES(%s, %s);''', (x, y))
	cursor.execute('select * from numbers order by val;')
	conn.commit()
	print("==========Inserted Into Database==============")
	count+=1

	xData.append(x)
	yData.append(y)


cursor.execute('''SELECT * FROM numbers ORDER BY val;''')
conn.commit()
conn.close()


plt.plot(yData, xData, marker='o', linestyle='-', color='r', label='values')
plt.title('Sample Data Plot')
plt.ylabel('Temperature')
plt.xlabel('Time')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sampleTemp.png")
plt.show()
plt.close()
