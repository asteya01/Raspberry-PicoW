from machine import Pin
import time

num = 0

led = Pin("LED", Pin.OUT)

while True:
    led.value(1)  # LED on
    time.sleep(0.5)
    num = num + 1
    print(num)
    if num > 6:
        break
    else:
        time.sleep(0.5)
        led.value(0) #LED off
        time.sleep(0.5)
        
