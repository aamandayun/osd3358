import smbus
import time
import socket

HOST = 'localhost'
PORT = 12345

bus = smbus.SMBus(0)
#bus = smbus.SMBus(2) #bus number
address = 0x48

while True:
	temp = bus.read_byte_data(address, 0) # 0 is the register to read
	print(temp, " Celcius")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			conn.send(str(temp).encode())
	time.sleep(0.5)
