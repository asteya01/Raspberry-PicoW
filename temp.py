import machine
import time
import uos

# Global hardware setup
led = machine.Pin("LED", machine.Pin.OUT)
temp_sensor = machine.ADC(4)  # Onboard temperature sensor

def read_temp():
    reading = temp_sensor.read_u16()
    voltage = reading * (3.3 / 65535)
    celsius = 27 - (voltage - 0.706) / 0.001721
    fahrenheit = (celsius * 9/5) + 32
    return celsius, fahrenheit

# Initialize log file
log_file = "temp_log.txt"
with open(log_file, "w") as f:
    f.write("Time,Celsius,Fahrenheit\n")

# Timer callback function
def log_temp(t):
    celsius, fahrenheit = read_temp()
    blink_rate = 0.2 if celsius > 40 else 1.0  # Fast blink if hot
    led.value(1)
    time.sleep(blink_rate)
    led.value(0)
    time.sleep(blink_rate)
    
    with open(log_file, "a") as f:
        f.write(f"{time.ticks_ms()},{celsius:.2f},{fahrenheit:.2f}\n")
    print(f"Temp: {celsius:.1f}°C ({fahrenheit:.1f}°F)")

# Start logging every 10 seconds
timer = machine.Timer()
timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=log_temp)

print("Temperature logger started! Check shell every 10s.")
