from rpi_ws281x import *
import argparse
import time

LED_1_COUNT      = 116      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1
LED_1_STRIP      = ws.WS2811_STRIP_RGB

LED_2_COUNT      = 220      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 9      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 1       # 0 or 1
LED_2_STRIP      = ws.WS2811_STRIP_RGB

def setColor(strips, color):
	for strip in strips:
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, color)
	for strip in strips:
		strip.show()

def wipeOut(strips):
	for strip in strips:
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0, 0, 0))
			strip.show()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
	parser.add_argument('-f', '--front', action='store_true', help='turn on front light')
	parser.add_argument('-s', '--side', action='store_true', help='turn on side light')
	args = parser.parse_args()

	stripFront = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL)
	stripSide = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL)

	stripFront.begin()
	stripSide.begin()

	try:
		strips = []
		if not args.front and not args.side:
			strips = [stripFront, stripSide]
		if args.front:
			strips.append(stripFront)
		if args.side:
			strips.append(stripSide)

		setColor(strips, Color(0, 0, 0))
		for i in range(100):
			setColor(strips, Color(255 * i // 100, 120 * i // 100, 90 * i // 100))
			time.sleep(0.03)

		while True:
			time.sleep(1)


	except KeyboardInterrupt:
		if args.clear:
			wipeOut(strips)
			