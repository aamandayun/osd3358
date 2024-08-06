#include "/opt/source/OSD3358-SM-RED-Peripherallibrary/libraries/rc_usefulincludes.h"
#include "/opt/source/OSD3358-SM-RED-Peripherallibrary/libraries/redperipherallib.h"
#include "/opt/source/OSD3358-SM-RED-Peripherallibrary/libraries/tmp468/rc_tmp468_defs.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

#define TMP_ADDR 0x48
#define I2C_BUS "/dev/i2c-0" //is this right??
#define SERVER_IP "192.168.7.2"
#define SERVER_PORT 12345
int main(){

	int file;
	char *filename = I2C_BUS;
	int addr = 0x48;

	if((file=open(filename, O_RDWR))<0){
		perror("failed to open bus");
	}


	int sockfd;
	struct sockaddr_in server_addr;
	char message[1024];
	
	//create a socket
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if(sockfd < 0){
		perror("error creating socket");
		exit(1);
	}
	
	//sets server address structure
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(SERVER_PORT);
	inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);	
	

	int ret;
	double temp_val;
	
	//ret = tmp468_initialize();
	/*
	if(ret != 0){
		printf("exiting\n");
		return 0;
	}*/

	if(read(file, &temp_val, sizeof(temp_val)) != sizeof(temp_val)){
		perror("Failed");
	}else{
		float temperature = temp_val /256.0;
		printf("Temperature: %.2f\n", temperature);

	}
	sleep(2);
	
//	temp_val = tmp468_read_temp(TMP468_CHANNEL_LOC);

	//connect to server
	if(connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0){
		perror("Error connecting to server");
		exit(1);
	}	

	//sends temp data
	sprintf(message, "Temperature: %.2f", temp_val);
	send(sockfd, message, strlen(message), 0);

	close(sockfd);
	
	return 0;


}
    
