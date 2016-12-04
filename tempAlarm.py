import RPi.GPIO as GPIO
import time
import socket
from bluetooth import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

server_sock = BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
uuid =  "00000000-0000-1000-8000-00805F9B34FB"

advertise_service( server_sock, "raspberrypi",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

def led_toggle():
    for i in range(3):
        GPIO.output(led_pin1, True)
        GPIO.output(led_pin2, True)
        time.sleep(1)
        GPIO.output(led_pin1, False)
        GPIO.output(led_pin2, False)
        time.sleep(1)
        
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


try: 
    while True:
        data = client_sock.recv(1024)
        if (data == "exit"): break
        print("received [%s]"%data)

        #LED Control PRT
        if (data == "0"):
            GPIO.output(led_pin1, False)
            GPIO.output(led_pin2, False)
        elif (data == "2"):
            GPIO.output(led_pin1, True)
            GPIO.output(led_pin2, True)
            #server_sock.send(bytes([data]))
            print "sending [%s]" % data   
        elif (data == "3"):
            led_toggle()

except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
        
