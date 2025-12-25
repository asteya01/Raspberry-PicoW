from machine import Pin
import time

num = 66

led = Pin("LED", Pin.OUT)

if num % 2 == 0:
    time.sleep(0.5)
    led.value(0) #LED off
    time.sleep(0.5)
else:
    time.sleep(0.5)
    led.value(1) #LED on
    time.sleep(0.5)
        
    
        

