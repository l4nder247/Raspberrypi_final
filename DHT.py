from gpiozero import OutputDevice, InputDevice
import time

class DHT11:
    MAX_DELAY_COUNT   = 100
    BIT_1_DELAY_COUNT = 10
    BITS_LEN          = 40

    def __init__(self, pin, pull_up=False):
        self._pin     = pin
        self._pull_up = pull_up

    def read_data(self):
        bit_count   = 0
        delay_count = 0
        bits        = ""

        # send start
        gpio = OutputDevice(self._pin)
        gpio.off()
        time.sleep(0.02)
        gpio.close()

        # switch to input, wait for response
        gpio = InputDevice(self._pin, pull_up=self._pull_up)
        while gpio.value == 1:
            pass

        # read 40 bits
        while bit_count < self.BITS_LEN:
            while gpio.value == 0:
                pass
            while gpio.value == 1:
                delay_count += 1
                if delay_count > self.MAX_DELAY_COUNT:
                    break
            bits += "1" if delay_count > self.BIT_1_DELAY_COUNT else "0"
            delay_count = 0
            bit_count  += 1

        # parse
        h_int   = int(bits[0:8],   2)
        h_dec   = int(bits[8:16],  2)
        t_int   = int(bits[16:24], 2)
        t_dec   = int(bits[24:32], 2)
        chk_sum = int(bits[32:40], 2)

        # verify
        if chk_sum != (h_int + h_dec + t_int + t_dec):
            return None, None

        humidity    = float(f"{h_int}.{h_dec}")
        temperature = float(f"{t_int}.{t_dec}")
        return humidity, temperature
