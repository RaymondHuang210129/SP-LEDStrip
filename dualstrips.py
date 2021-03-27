import rpi_ws281x as rpiws
import time
from datetime import datetime

class DualStrips:
	def __init__(self, led_1_count, led_1_pin, led_1_freq_hz, led_1_dma, led_1_invert, led_1_brightness, led_1_channel, led_2_count, led_2_pin, led_2_freq_hz, led_2_dma, led_2_invert, led_2_brightness, led_2_channel, reverse_idx=False):
		self.__strip1 = rpiws.Adafruit_NeoPixel(led_1_count, led_1_pin, led_1_freq_hz, led_1_dma, led_1_invert, led_1_brightness, led_1_channel)
		self.__strip2 = rpiws.Adafruit_NeoPixel(led_2_count, led_2_pin, led_2_freq_hz, led_2_dma, led_2_invert, led_2_brightness, led_2_channel)
		self.__led1Count = led_1_count
		self.__led2Count = led_2_count
		self.__reverseIdx = reverse_idx
		self.__lastShowTime = datetime.utcnow()
		self.__isStrip1Modified = False
		self.__isStrip2Modified = False

	def begin(self):
		self.__strip1.begin()
		self.__strip2.begin()

	def show(self):
		if self.__isStrip1Modified:
			self.__strip1.show()
			self.__isStrip1Modified = False
		if self.__isStrip2Modified:
			self.__strip2.show()
			self.__isStrip2Modified = False

	def setPixelColor(self, n, color):
		if n > self.__led1Count + self.__led2Count:
			raise RuntimeError('led position out of index (the led counts are %d and %d)' % (self.__led1Count, self.__led2Count))
		if self.__reverseIdx:
			if n >= self.__led2Count:
				self.__strip1.setPixelColor(self.__led1Count + self.__led2Count - n, color)
				self.__isStrip1Modified = True
			else:
				self.__strip2.setPixelColor(self.__led2Count - n, color)
				self.__isStrip2Modified = True
		else:
			if n > self.__led1Count:
				self.__strip2.setPixelColor(n - self.__led1Count, color)
				self.__isStrip2Modified = True
			else:
				self.__strip1.setPixelColor(n, color)
				self.__isStrip1Modified = True

	def setPixelColorRGB(self, n, red, green, blue, white = 0):
		if n > self.__led1Count + self.__led2Count:
			raise RuntimeError('led position out of index (the led counts are %d and %d)' % (self.__led1Count, self.__led2Count))
		if self.__reverseIdx:
			if n >= self.__led2Count:
				self.__strip1.setPixelColor(self.__led1Count + self.__led2Count - n, rpiws.Color(red, green, blue, white))
				self.__isStrip1Modified = True
			else:
				self.__strip2.setPixelColor(self.__led2Count - n, rpiws.Color(red, green, blue, white))
				self.__isStrip2Modified = True
		else:
			if n > self.__led1Count:
				self.__strip2.setPixelColor(n - self.__led1Count, rpiws.Color(red, green, blue, white))
				self.__isStrip2Modified = True
			else:
				self.__strip1.setPixelColor(n, rpiws.Color(red, green, blue, white))
				self.__isStrip1Modified = True

	def setBrightness(self, brightness):
		raise NotImplementedError

	def getBrightness(self):
		raise NotImplementedError

	def getPixels(self):
		pixelData = []
		pixelData.extend(self.__strip1.getPixels())
		pixelData.extend(self.__strip2.getPixels())
		if self.__reverseIdx:
			return pixelData.reverse()
		else:
			return pixelData

	def numPixels(self):
		return self.__strip1.numPixels() + self.__strip2.numPixels()

	def getPixelColor(self, n):
		if n > self.__led1Count + self.__led2Count:
			raise RuntimeError('led position out of index (the led counts are %d and %d)' % (self.__led1Count, self.__led2Count))
		if self.__reverseIdx:
			if n > self.__led2Count:
				self.__strip1.getPixelColor(self.__led1Count + self.__led2Count - n)
			else:
				self.__strip2.getPixelColor(self.__led2Count - n)
		else:
			if n > self.__led1Count:
				self.__strip2.getPixelColor(n - self.__led1Count)
			else:
				self.__strip1.getPixelColor(n)

	def setReverseIdx(self, isReverse):
		self.__reverseIdx = isReverse

if __name__ == '__main__':
	print('dualstrips API debug test')

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

	strip = DualStrips(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL)

	strip.begin()

	for i in range(strip.numPixels()):
		strip.setPixelColor(i, rpiws.Color(0, 0, 0))
	strip.show()

	for t in range(50):

		for i in range(strip.numPixels()):
			strip.setPixelColor(i, rpiws.Color(255, 0, 0))
			strip.show()
			time.sleep(0.01)

		strip.setReverseIdx(True)
		time.sleep(1)

		for i in range(strip.numPixels()):
			strip.setPixelColor(i, rpiws.Color(0, 255, 0))
			strip.show()
			time.sleep(0.01)

		strip.setReverseIdx(False)
		time.sleep(1)

