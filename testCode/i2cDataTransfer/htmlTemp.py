from flask import Flask, jsonify
import smbus
import time

app = Flask(__name__)

# Initialize I2C bus
bus = smbus.SMBus(0)  # Use 1 for Raspberry Pi 2 or 3, use 0 for older models

@app.route('/temperature')
def get_temperature():
	print("here")
	address = 0x48  # I2C device address
	register = 0    # Register to read

	try:
		temp = bus.read_byte_data(address, register)
		print(temp)
		return jsonify({'temperature': temp})
	except Exception as e:
		return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')  # Run the server on all available IPs

