import RPi.GPIO as GPIO
import time
import socket
from bluetooth import *
from subprocess import *


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

bus = smbus.SMBus(1)
addr = 0x40
addr_temp = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe

pir = 24
gpio_pin = 13
led_pin1 = 14
led_pin2 = 15
GPIO.setup(pir, GPIO.IN)
GPIO.setup(gpio_pin, GPIO.OUT)
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

temp = 0.0
humi = 0.0
val = 0
data = [0, 0]

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output= p.communicate()
    return output

try:
    bus.write_byte(addr, soft_reset)
    time.sleep(0.05)
    p = GPIO.PWM(gpio_pin, 100)	
    while True:
        bus.write_byte(addr, cmd_temp)
        time.sleep(0.260)
        for i in range(0,2,1):
            data[i] = bus.read_byte(addr)
        val = data[0] << 8 | data[1]
 
        temp = -46.85 + 175.72/65536*val
        bus.write_byte(addr, cmd_humi)
        time.sleep(0.260)
	
        for i in range(0,2,1):
            data[i] = bus.read_byte(addr)
        val = data[0] << 8 | data[1]
        humi = -6.0+125.0/65536*val;
	
	if (temp > 22):
            
        else:
            string_temp = str(temp)
            conn.send(string_temp)
		
        # if temperature is higher than 22	
        if(temp > 22):
		cmd = "echo Indoor Temperature is so HOT! > /dev/rfcomm0"
                run_cmd(cmd)		
		string_temp = str(temp)
            	conn.send(string_temp)
	# if temperature is lower than 22
	if(temp <= 22):
                cmd = "echo Indoor Temperature is so COLD! > /dev/rfcomm0"
                run_cmd(cmd)
		string_temp = str(temp)
            	conn.send(string_temp)
		
	# if humidity is higher than 60%
        if(humi > 60):
		cmd = "echo Indoor Humidity is so HIGH! > /dev/rfcomm0"
                run_cmd(cmd)
		string_humi = str(humi)
            	conn.send(string_humi)
	# if humidity is lower than 60%
	if(humi <= 60):
                cmd = "echo Indoor Humidity is so LOW! > /dev/rfcomm0"
                run_cmd(cmd)
		string_humi = str(humi)
            	conn.send(string_humi)
		
        else:
            GPIO.output(led_pin1, False)
            GPIO.output(led_pin2, False)
            p.stop()
        print 'temp : %.2f, humi: %.2f' %(temp, humi)
        time.sleep(1)
    
except IOError:
    pass
