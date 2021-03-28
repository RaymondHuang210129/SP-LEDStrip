import math

class GammaColor:

	def __init__(self):
		pass

	def make(self, red, green, blue, white=0, gamma=2.8, maxRed=255, maxGreen=120, maxBlue=90):
		trueRed = int(math.pow(red / 255, gamma) * maxRed + 0.5)
		trueGreen = int(math.pow(green / 255, gamma) * maxGreen + 0.8)
		trueBlue = int(math.pow(blue / 255, gamma) * maxBlue + 0.8)
		return (white << 24) | (trueRed << 16) | (trueGreen << 8) | trueBlue

class OriginColor:

	def __init__(self):
		pass

	def make(self, red, green, blue, white=0):
		return (white << 24) | (red << 16) | (green << 8) | blue
