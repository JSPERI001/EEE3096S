import RPi.GPIO as GPIO
import time
import os
import spidev
import sys
from time import sleep

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
        volts = (data * 3.3) / float(1023)
        volts = round(volts,places)
        return volts

# Function to calculate temperature
def ConvertTemp(data,places):
        temp = ((data * 330)/float(1023))-50
        temp = round(temp,places)
        return temp

# Define sensor channels
light_channel = 0
temp_channel  = 1
pot_channel = 2

# Define delay between readings
freq = 0.5

GPIO.setmode(GPIO.BCM)

switch1 = 17    #Reset
switch2 = 27    #Frequency
switch3 = 22    #Stop
switch4 = 24    #Display

GPIO.setup(switch1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(switch3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(switch4, GPIO.IN, pull_up_down = GPIO.PUD_UP)