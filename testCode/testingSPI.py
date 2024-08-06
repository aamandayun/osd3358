import spidev

spi0 = spidev.SpiDev(0, 0)  # SPI0, device 0
spi1 = spidev.SpiDev(0, 1)  # SPI0, device 1

try:
    spi1.open(0, 1)  # Open SPI1, device 1
    print("SPI device opened successfully")

    send_data = [0xAA, 0xBB, 0xCC, 0xDD]
    print("Sending:", send_data)

    received_data = spi1.xfer(send_data)
    print("Received:", received_data)

except Exception as e:
    print("Error:", e)

finally:
    spi1.close()
    print("SPI device closed")

