#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
//#include </usr/include/linux/ioctl.h>
#include <sys/ioctl.h>
#include </usr/include/linux/spi/spidev.h>


uint8_t mode = 0; //spi mode specification
uint32_t speed = 500000; //spi speed
uint8_t bits = 8; //bits to spi send


void spi_transfer(int fd, uint8_t *data, int length){
	struct spi_ioc_transfer spi[length];
	
	//setup transfer struct
	//initalize struct with all 0's
	for(int i=0; i<length; i++){
		memset(&spi[i], 0, sizeof(struct spi_ioc_transfer));
		spi[i].tx_buf = (unsigned long) (data+i); //buffer, pointer to the variable we want to send out
		spi[i].rx_buf = (unsigned long) (data+i); //where we want to store incoming data
		spi[i].len = 1; //length in bites that we want to transfer
		spi[i].speed_hz = speed;
		spi[i].bits_per_word = bits;
	}

	//check the performance of the SPI data transfer
	if(ioctl(fd, SPI_IOC_MESSAGE(length), spi)<0){
		perror("error performing SPI data transfer");
		close(fd);
		exit(-1);
	}
}



int main(int argc, char * argv[]){
	int fd; //file descriptor
	uint8_t data[3]; //array for output data

	//***** open SPI bus file descriptor ***********

	fd = open("/dev/spidev0.0", O_RDWR); //open with read and write
	if(fd<0){
		perror("error opening file descriptor");
		return -1;
	}else{
		printf("===Loaded bus file Correctly===\n");
	}


	//*** Setup of the SPI bus *** 
	if(ioctl(fd, SPI_IOC_WR_MODE, &mode) < 0){  //setting up SPI mode
		perror("error setting up SPI mode");
		return -1;
	}

	if(ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed) < 0){ //setting up SPI speed
		perror("error setting up SPI speed");
		return -1;
	}

	if(ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits)<0){ //setting up SPI bits
		perror("error setting up SPI bits");
		return -1;
	}

	printf("===Ready for SPI accesses===\n");

	//need to setup GPIO's direction
	data[0] = 0x40; //indicates that you want to do a write
	data[1] = 0x0; //address you want to write to
	data[2] = 0xfe; //data you want to write out	
	spi_transfer(fd, data, 3);

	//set LED
	data[0] = 0x40; //indicates that you want to do a write
	data[1] = 0xa; //address you are writing to

	if(argc > 1){
		data[2] = atoi(argv[1])>0;
	}else{
		data[2] = 0x0;
	}
	spi_transfer(fd, data, 3);


	//Read button
	data[0] = 0x41; //indicates that you want to do a read
	data[1] = 0x9; //address you are reading from
	data[2] = 0x00; //we don't care
	spi_transfer(fd, data, 3);
	printf("Button is %s\n", ((data[2] & (1<<1))>0)? "pressed" : "not pressed");
	
	close(fd);

	return 0;
}
