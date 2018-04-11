#!/usr/bin/env python
import socket
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
GPIO.setmode(GPIO.BCM)

SERVERIP = '10.0.0.43'
n = 0
#hook the sound sensor into ground and power
#Hook the PCF into power and ground
#hook the PCF SCl pin into GPIO 3 (SCL)
#Hook the PCF SDA pin into GPIO 2 (SDA)
#Plug in the sound sensors SIG pin into a disconnect
#Plug in the PCF Ain0 into the disconnect with the SIG plug fron the sensor


def setup():
    ADC.setup(0x48)


def loop():
    count = 0
    n = 0
    while True:
        voiceValue = ADC.read(0)
        if voiceValue:
            print (('Value:', voiceValue))
            lcd.message(" voice detected ")
        lcd.message("\n %s %%" % (voiceValue))
        if voiceValue < 50:
                print (("Voice detected! ", count))
        count += 1
        lcd.message("\n %s %%" % (voiceValue))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVERIP, 8881))
        print "%d : Connected to server" % n,
        data = "'reason to shut up',%d, %s %%" % (n, voiceValue)
        sock.sendall(data)
        print " Sent:", data
        sock.close()
        n += 1
        time.sleep(30.0)

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass