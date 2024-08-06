import spidev
import time

def spi_test(spi_bus, spi_device):
	spi = spidev.SpiDev()
	spi.open(spi_bus, spi_device)

	try:
		spi.max_speed_hz = 10000000
		spi.mode = 0
		spi.bits_per_word = 8

		tx_data = [170, 187, 204, 221]
		print(f"Sending from {spi_bus} t p {spi_device}: {tx_data}")
		rx_data = spi.xfer2(tx_data)

		print(f"received from {spi_device}: {rx_data}")

	finally:
		spi.close()


if __name__ ==  "__main__":
	spi_test(0,0)
	time.sleep(1)
	spi_test(1, 0)
