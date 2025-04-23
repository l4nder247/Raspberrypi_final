###THIS IS THE CODE FOR THE HUMIDITY AND TEMP STATION
#final_py_iteration2.py is the iteration with everything added 
import BlynkLib
from BlynkTimer import BlynkTimer
from DHT import dht11 # Make sure your file is renamed appropriately (e.g., dht_module.py)
import time
import adafruit_bmp280 # run this command "sudo pip3 install adafruit-circuitpython-bmp280 --break-system-packages"
import board
import smtplib
from email.mime.text import MIMEText


import csv
import os


# Initialize DHT11
dht11 = dht11(23)
# Intialize the thang
i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
bmp280.sea_level_pressure = 1023.6  ########THIS LINE NEEDS TO BE CHANGED FOR THE DAILY AIR PRESSURE

# you can do bmp280.temperature/pressure/altitude, and assign it to a varialbe where you can update it to blynk.
#print(bmp280.temperature)
#print(bmp280.pressure)
#print(bmp280.altitude)

#create new csv file each time you run based on current date/time
current_time = time.strftime("%Y-%m-%d %H:%M:%S")
CSV_FILE = f"weather_run_{current_time}.csv"


# Blynk Auth Token
BLYNK_AUTH = "JIaOzPa0-NvwUkd6kB7AOoaO2JHnSWHr"

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer instance
timer = BlynkTimer()
original_dir = os.getcwd()
data_folder = os.path.join(original_dir, 'datafiles')

def hello_world():
    print("Start!")
# blynk.virtual_write(5, 25)
def publish_data():
    email_timer = 6
    #blynk.virtual_write(5, 25)
    result = dht11.read_data()
    print("Raw result from DHT11:", result)
    while True:             
        os.chdir(original_dir)
        TEMP_THRESHOLD=10
        HUMIDITY_THRESHOLD = 70
        temp = result[1]
        hum = result[0]
        pressure = bmp280.pressure

        alert_msg = ""
        try:
            if temp > TEMP_THRESHOLD:
                alert_msg = f"High Temperature Alert: {temp}°C\n"

            if hum > HUMIDITY_THRESHOLD:
                alert_msg = f"High Humidity Alert: {hum}%\n"

            if ((len(alert_msg)!=0) and (email_timer >10)):
                msg = MIMEText(alert_msg)
                msg['Subject'] = 'RPI Weather Alert'
                msg['From'] = 'lucarasberrypi@gmail.com'
                msg['To'] = 'landersb.tenzer@gmail.com'

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login('lucarasberrypi@gmail.com', 'xqpy cmus qlsn ehtb')
                    server.send_message(msg)
                    print("Alert email sent.")
                    #reset the email timer
                    
                    email_timer = 0
        except TypeError as e:
            #sometimes, the temperature sensor likes to trip, and not work. This catches the error when trying to compare temp to temp_threshold, which throws a TypeError
            print("Type Error ExceptionCaught: Hum and temp values empty")
        
        print()
        print(f"Temperature: {temp}\n")
        blynk.virtual_write(5, temp)
        print(f"Humidity: {hum}\n")
        blynk.virtual_write(4, hum)
        print(f"Pressure: {pressure}\n\n")
        blynk.virtual_write(1, pressure)
        time.sleep(2)
        email_timer = email_timer + 1
        
        
        #Swap to the data directory
        os.chdir(data_folder)
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, temp, hum, pressure])

# Add Timers
timer.set_timeout(2, hello_world)
timer.set_interval(3, publish_data)

# Main loop
while True:
    blynk.run()
    timer.run()
