from machine import I2C, Pin
import time
from as7341 import AS7341

# --- SETUP ---
# Initialize I2C and Sensor
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
sensor = AS7341(i2c)
sensor.enable()

# --- CONFIGURATION ---
# Turn off LED to measure ambient light
if hasattr(sensor, 'led'):
    sensor.led = False
if hasattr(sensor, 'set_led_current'):
    sensor.set_led_current(0)

# Set Gain (Sensitivity)
# 1=1x, 2=2x, 3=4x, 4=8x, etc.
sensor.set_again(3)  

# Set Integration Time
# These settings determine how long the sensor "stares" at the light
sensor.set_atime(29)   # ~50ms
sensor.set_astep(599)

print("Sensor Initialized. Open 'View > Plotter' to see graph.")

# --- MAIN LOOP ---
while True:
    try:
        # 1. Read Low Channels (F1-F4)
        # 'True' usually enables the lower bank
        sensor.set_spectral_measurement(True)
        time.sleep(0.15) # Wait slightly longer than integration time (50ms)
        data_low = sensor.get_spectral_data()
        
        # 2. Read High Channels (F5-F8)
        # 'False' switches to the higher bank
        sensor.set_spectral_measurement(False)
        time.sleep(0.15)
        data_high = sensor.get_spectral_data()

        # 3. Format Data for Thonny Plotter
        # The plotter wants one line of text: "Key1:Value1, Key2:Value2, ..."
        # We combine data_low and data_high into one print statement so they graph together.
        
        # data_low indices:  0=F1(Violet), 1=F2(Indigo), 2=F3(Blue), 3=F4(Cyan)
        # data_high indices: 0=F5(Green),  1=F6(Yellow), 2=F7(Orange), 3=F8(Red)
        
        # We print the clearest colors to keep the graph readable:
        print(f"Violet:{data_low[0]}, Blue:{data_low[2]}, Green:{data_high[0]}, Red:{data_high[3]}, Clear:{data_low[4]}")

        # Note: If you want ALL channels, uncomment the line below instead:
        # print(f"F1:{data_low[0]}, F2:{data_low[1]}, F3:{data_low[2]}, F4:{data_low[3]}, F5:{data_high[0]}, F6:{data_high[1]}, F7:{data_high[2]}, F8:{data_high[3]}")

        # Small delay to control graph speed
        time.sleep(0.1)

    except OSError as e:
        # Ignore occasional I2C read errors to keep the graph moving
        print(f"Sensor error: {e}")
        time.sleep(0.5)
