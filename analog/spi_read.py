from time import time, sleep
import math
import sys

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

SPI_PORT = 0
SPI_DEVICE = 1
CHANNEL = 3

if(len(sys.argv) > 3):
    SPI_PORT = int(sys.argv[1])
    SPI_DEVICE = int(sys.argv[2])
    CHANNEL = int(sys.argv[3])

SAMPLING_RATE = 1.000
REPORTING_RATE = 1.000
if(len(sys.argv) > 5):
    SAMPLING_RATE = float(sys.argv[4]) / 1000
    REPORTING_RATE = float(sys.argv[5]) / 1000

defaultSPI = True
if (len(sys.argv) > 9):
    SPI_CLK = int(sys.argv[6])
    SPI_DI = int(sys.argv[7])
    SPI_DO = int(sys.argv[8])
    SPI_CS = int(sys.argv[9])
    defaultSPI = False

if defaultSPI:
    spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE)
else:
    gpio = GPIO.get_platform_gpio()
    spi = SPI.BitBang(gpio, SPI_CLK, SPI_DI, SPI_DO, SPI_CS)

values = []
last_report = 0

def sampledData(value):
    global values
    if not math.isnan(value):
        values.append(value)
    
def report():
    global values, last_report
    if (time() - last_report > REPORTING_RATE):
        last_report = time()
        if len(values) > 0:
            print('{0:0.3F},{1},{2:0.3F}'.format(time(),CHANNEL, sum(values)/len(values) ))
        maxInternal = 0
        values = []

def readChannel(channel):
    command = 0b10000001
    command = command + (channel << 4)
    results = spi.transfer([command, 0b0,0b0,0b0]);#//i
    left = results[3] >> 7
    middle = results[2] << 1
    right = results[1] << 9;#8
    final = left + middle + right
    return final

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
    value = readChannel(CHANNEL)
    sampledData(value)
    report()
    sleep(SAMPLING_RATE)