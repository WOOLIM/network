#!/usr/bin/hon
import socket
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO to LCD mapping
LCD_RS = 23
#LCD_RW = 24
LCD_E = 26
LCD_D4 = 17
LCD_D5 = 18
LCD_D6 = 27
LCD_D7 = 22

# Define some device constants
LCD_WIDTH = 16 # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

HOST='203.153.148.121'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

gpio_pin = 13
GPIO.setup(gpio_pin, GPIO.OUT)

def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)
    
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True for character
    # False for command
    GPIO.output(LCD_RS, mode) # RS
    
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enablp = GPIO.PWM(gpio_pin, 100)e' pin
    lcd_toggle_enable()
    
def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message,line):
    # Send string to display
    message = message.ljust(LCD_WIDTH," ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

try:
    p = GPIO.PWM(gpio_pin, 100)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT) # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7

    lcd_init()
    
    while 1:
        data=s.recv(8096)
        if data>='Warning':
            p.start(100)
            p.ChangeDutyCycle(90)
            p.ChangeFrequency(329)
            lcd_string("Warning! Somone Approach",LCD_LINE_1)
          
    else:
        p.stop()
        lcd_string("Safe State",LCD_LINE_1)
    
    while 1:
        data=s.recv(8096)
        if data>='Warning':
            p.start(100)
            p.ChangeDutyCycle(90)
            p.ChangeFrequency(329)
            lcd_string("Warning! Somone Approach",LCD_LINE_1)
            
            
            lcd_string("temp is %s" % (data),LCD_LINE_2)
            time.sleep(2) 
            print 'temp is high'
     
        else:
            p.stop()
            lcd_string("Baby is safe",LCD_LINE_1)
            lcd_string("temp is %s" % (data),LCD_LINE_2)
            time.sleep(2)
            print 'temp is low'
    s.close()

except KeyboardInterrupt:
        pass
