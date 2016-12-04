import smbus
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
bus = smbus.SMBus(1)
addr = 0x40
 
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe
 
gpio_pin = 13
led_pin1 = 14
led_pin2 = 15
GPIO.setup(gpio_pin, GPIO.OUT)
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)
 
temp = 0.0
humi = 0.0
val = 0
data = [0, 0]
 
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
	
	# if temperature is higher than 32	
	if(temp > 25):
            p.start(100)
            p.ChangeDutyCycle(90)
            p.ChangeFrequency(329)
            GPIO.output(led_pin1, True)
	    GPIO.output(led_pin2, True)
        else:
	    GPIO.output(led_pin1, False)
	    GPIO.output(led_pin2, False)
	    p.stop()
        print 'temp : %.2f, humi: %.2f' %(temp, humi)
        time.sleep(1)
except KeyboardInterrupt:
    pass
