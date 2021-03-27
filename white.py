# Author: Raymond Huang (raymond210129.cs05@g2.nctu.edu.com)
# Credit: Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)

import rpi_ws281x as rpiws
from dualstrips import DualStrips 
import argparse
import time

LED_1_COUNT      = 116      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1
LED_1_STRIP      = rpiws.ws.WS2811_STRIP_RGB

LED_2_COUNT      = 220      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 9      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 1       # 0 or 1
LED_2_STRIP      = rpiws.ws.WS2811_STRIP_RGB

def setColor(strip, color):
	for i in range(strip.numPixels()):
			strip.setPixelColor(i, color)
	strip.show()

def wipeOut(strips):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, rpiws.Color(0, 0, 0))
		strip.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
	parser.add_argument('-f', '--front', action='store_true', help='turn on front light')
	parser.add_argument('-s', '--side', action='store_true', help='turn on side light')
	args = parser.parse_args()

	if (not args.front and not args.side) or (args.front and args.side):
		strip = DualStrips(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL)
	elif args.front:
		strip = rpiws.Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL)
	else:
		strip = rpiws.Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL)
	strip.begin()

	try:
		setColor(strip, rpiws.Color(0, 0, 0))
		for i in range(100):
			setColor(strip, rpiws.Color(255 * i // 100, 120 * i // 100, 90 * i // 100))
			time.sleep(0.03)

		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		if args.clear:
			wipeOut(strip)
			