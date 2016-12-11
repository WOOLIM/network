#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import socket
from bluetooth import *
from subprocess import *
import smbus
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

bus = smbus.SMBus(1)
addr_gg = 0x40
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

HOST='203.153.148.121'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr=s.accept()
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print 'Connected by', addr

while True:
    bus.write_byte(addr_gg, soft_reset)
    time.sleep(0.05)
    p = GPIO.PWM(gpio_pin, 100)	
    while True:
        bus.write_byte(addr_gg, cmd_temp)
        time.sleep(0.260)
        for i in range(0,2,1):
            data[i] = bus.read_byte(addr_gg)
        val = data[0] << 8 | data[1]
        temp = -46.85 + 175.72/65536*val
        print(temp)
        
        if (temp > 22):
            string_temp = str(temp)
            conn.send(string_temp)
        else:
            string_temp = str(temp)
            conn.send(string_temp)
s.close()
