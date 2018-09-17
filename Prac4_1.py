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

count = 0
x = 0
y = 0
timer = 0

try:
        while (1):

                if GPIO.input(switch1) == 0:
                        x = 0
                        timer = 0
                        os.system('clear')
                        time.sleep(0.25)

                if GPIO.input(switch2) == 0:
                       count = count + 1

                       if count == 1:
                               freq = 0.5
                               print("500ms")
                       if count == 2:
                               freq = 1
                               print("1s")
                       if count == 3:
                               freq = 2
                               print("2s")
                               count = 0
                       time.sleep(0.25)

                if GPIO.input(switch3) == 0:
                        if(y==0):
                                y=1
                                print("on")
				print("--------------------------------------------")
                                print("Time"+"\t"+"\t"+"Timer"+"\t"+"Pot"+"\t"+"Temp"+"\t"+"Light")
                        else:
                                y=0
                                print("off")
                        time.sleep(.25)
		if (y==1):
			
			# Read the light sensor data
                        light_level = ReadChannel(light_channel)
                        light = 100 - ((light_level - 40)/float(983))*100
                        light = round(light,0)

                        # Read the temperature sensor data
			temp_level = ReadChannel(temp_channel)
                        temp_volts = ConvertVolts(temp_level,2)
                        temp       = ConvertTemp(temp_level,2)

                        #Read POT Values
                        pot_level = ReadChannel(pot_channel)
                        pot = ConvertVolts(pot_level,1)

                        timeC = time.strftime("%I")+ ':' + time.strftime("%M") + ':' + time.strftime("%S")
                        print("{}       {}s     {}V     {}C     {}%".format(timeC,timer,pot,temp,light))
                        time.sleep(freq)
                        timer = timer + freq
			
		if(y==0):
			
			if GPIO.input(switch4) == 0:
                                print("--------------------------------------------")
                                print("Time"+"\t"+"\t"+"Timer"+"\t"+"Pot"+"\t"+"Temp"+"\t"+"Light")

                                for i in range (0,5):
                                # Read the light sensor data
                                light_level = ReadChannel(light_channel)
                                light = 100 - ((light_level - 40)/float(983))*100
                                light = round(light,0)

                                # Read the temperature sensor data
                                temp_level = ReadChannel(temp_channel)
                                temp_volts = ConvertVolts(temp_level,2)
                                temp       = ConvertTemp(temp_level,2)

                                 #Read POT Values
                                 pot_level = ReadChannel(pot_channel)
                                 pot = ConvertVolts(pot_level,1)

                                 timeC = time.strftime("%I")+ ':' + time.strftime("%M") + ':' + time.strftime("%S")
                                 print("{}       {}s     {}V     {}C     {}%".format(timeC,timer,pot,temp,light))
                                 time.sleep(freq)
                                 timer = timer + freq
                	timer = timer + freq
                	time.sleep(freq)
except KeyboardInterrupt:
        spi.close()


