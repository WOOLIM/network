import RPi.GPIO as GPIO
import time
import socket
from bluetooth import *
from subprocess import *

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output= p.communicate()
    return output

try: 
    cmd = "echo mommy help me > /dev/rfcomm0"
    run_cmd(cmd)
    #print(siba)

except IOError:
    pass
