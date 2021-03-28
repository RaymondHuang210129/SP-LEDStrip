import math

class GammaColor:

	def Color(red, green, blue, white=0, gamma=2.8, maxRed=255, maxGreen=120, maxBlue=90):
		trueRed = int(math.pow(red / 255, gamma) * (maxRed + 9) + 0.5)
		trueGreen = int(math.pow(green / 255, gamma) * (maxGreen + 4) + 0.8)
		trueBlue = int(math.pow(blue / 255, gamma) * (maxBlue + 3) + 0.8)
		#print(trueRed, trueGreen, trueBlue)
		return (white << 24) | (trueRed << 16) | (trueGreen << 8) | trueBlue
