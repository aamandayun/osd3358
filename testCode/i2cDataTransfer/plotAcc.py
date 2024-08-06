import numpy as np
import time
import datetime
import socket
import matplotlib
matplotlib.use('Agg')
from PIL import Image
from flask import Flask, send_file

import matplotlib.pyplot as plt

app = Flask(__name__)

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
                        print("acceleration received: " , data.decode())
                        print("\n")

                        x = datetime.datetime.now()
                        y = int(data.decode()) 

                        xData.append(x)
                        yData.append(y)
            # plt.plot(x, y)
                #plt.gcf().autofmt_xdate()
                        count+=1
                except ConnectionRefusedError as e:
                        print(f"Connection refused: {e}")
                        time.sleep(1)
                        continue

        time.sleep(0.5)


#plt.plot(xData, yData)
#plt.gcf().autofmt_xdate()
#print("saving plot")
#plt.savefig('tempChart.png')

plt.plot(xData, yData, marker='o', linestyle='-', color='b', label='Temperature')
plt.title('Accelerometer Plot')
plt.xlabel('Time')
plt.ylabel('acc')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("acc.png")

plt.show()
plt.close()
