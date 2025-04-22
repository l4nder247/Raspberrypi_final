###THIS IS THE CODE FOR THE HUMIDITY AND TEMP STATION
import BlynkLib
from BlynkTimer import BlynkTimer
from DHT11 import DHT11  # Make sure your file is renamed appropriately (e.g., dht_module.py)
import time
import adafruit_bmp280 # run this command "sudo pip3 install adafruit-circuitpython-bmp280 --break-system-packages"
import board

import csv
import os


# Initialize DHT11
dht11 = DHT11(17)
# Intialize the thang
i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
bmp280.sea_level_pressure = 1023.6  ########THIS LINE NEEDS TO BE CHANGED FOR THE DAILY AIR PRESSURE

# you can do bmp280.temperature/pressure/altitude, and assign it to a varialbe where you can update it to blynk.
print(bmp280.temperature)
print(bmp280.pressure)
print(bmp280.altitude)



# Blynk Auth Token
BLYNK_AUTH = "JIaOzPa0-NvwUkd6kB7AOoaO2JHnSWHr"

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer instance
timer = BlynkTimer()

def hello_world():
    print("Start!")
# blynk.virtual_write(5, 25)
def publish_data():
    #blynk.virtual_write(5, 25)
    result = dht11.get_result()
    print("Raw result from DHT11:", result)
    while True:
        print(f"Temperature: {result[2]}")
        blynk.virtual_write(5, result[2])
        print(f"Humidity: {result[1]}")
        blynk.virtual_write(4, result[1])
        print(f"Pressure: {bmp280.pressure}")
        blynk.virtual_write(1, bmp280.pressure)

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, tempVal, humVal])

# Add Timers
timer.set_timeout(2, hello_world)
timer.set_interval(3, publish_data)

# Main loop
while True:
    blynk.run()
    timer.run()