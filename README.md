# Raspberrypi_final

### Features
1. **Start with unusual import statments**
    - BlynkLib, BlynkTimer, `from DHT import dht11`
    - `import adafruit_bmp280`
    - `email.mime.text import MIMEText`

2. **Initializing BMP280 & dht11**
    the sensor becomes objects of their respective classes
    - `dht11 = dht11(gpioinput)`
    - `i2c = board.I2C()`
    - `bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)`
3. **Setting up the CSV**
    - Set a regex expression to retrieve current time, and name the csv file acordingly each time the script is ran. 
    - Set up the directories, so the script knows to jump back and forth

4. **Set up blynk**
   -`timer = BlynkTimer()`

5. **while True loop**:
    - Reintialize the directory back to the original after changing the csv
    - Retrieve the data based on indexing the array that is returned. 
    - **Email**
        - Conditionals statements decide what should be teh message body
        - Once the lenght of the message is not empty, and the email timer passes 20 seconds, it will send an email
        - The Try and the Catch block. 
            - Sometimes, the dht11 sensor does not collect data the first time, this will require the user to restart the script. The try and catch will stop the program from ending abruptly when that happens. 
            - It is a TypeError since if temperature is null, you can not compare a `TEMP_THRESHOLD`

6. **CSV File writing**
- Create writer object
- create timestamp variable, and then write to each row, temp, hum, pressure.

7. **While True main loop**
    `blynk.run()
    timer.run()`








<!-- // explain code in detail -->
<!-- // describe fucntion logic and algos -->
<!--relevant code snipets -->


