from flask import Flask, render_template
import smbus
import Adafruit_BBIO.GPIO as GPIO
import os

bus = smbus.SMBus(0)
address = 0x48

bus2 = smbus.SMBus(0)
address2=0x5c
app = Flask(__name__)

#GPIO
LED_PIN = "USR0"

GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/')
def index():
	temp = bus.read_byte_data(address,0)
	pressure = bus2.read_byte_data(address2, 0)

	print("hello")
	print(f"temp; {temp}")

	#for LEDS
	led_status = GPIO.input(LED_PIN)
	status = 'On' if led_status else 'Off';
	color = '#87D386' if status else '#BF2828';


	cpu_usage = os.popen("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1}'").read().strip()
	memory_usage = os.popen("free | grep Mem | awk '{print $3/$2 * 100.0}'").read().strip()

	print(f"cpu usage: {cpu_usage}")


	return render_template('index.html', temp=temp, pressure=pressure, status=status, color=color,
	cpu_usage=cpu_usage, memory_usage=memory_usage)


@app.route('/toggle', methods=['POST'])
def toggle():
	current_state = GPIO.input(LED_PIN)
	GPIO.output(LED_PIN, not current_state)

	return index()



if __name__=='__main__':
#	app.run(debug=True, host='192.168.7.2')
	app.run(debug=True, host='0.0.0.0')
