# Side Project: Control WS182B LED Strips Using RaspberryPi 4 #

I'm developing this project for the LED light strips in my bedroom. 

This Framework allows me to manage the hardware, create animations and make expansion more easily. The ultimate purpose is to make this system become easy deployable and help me to decorate other place in my house sooner or later.

The core library that I use, rpi_ws281x, allows the Raspberry Pi to controll up to two independent light strips. Based on this library, I further developed some add-on API for following occasion:

1. Need to seem two independent led strips as a long strip and design it's animation without knowing the border
2. Need to apply color profiles (e.g. gamma correction) instead of the original hardware color

These add-on APIs design allows developers to adapt the situation mentioned above simply by adding only several line of code. For example:

```python3
from rpi_ws281x import * ''' The original library '''
from dualstrips import DualStrips ''' The add-on library for strips merging '''
from colorProfile import OriginColor, GammaColor

if merge2Strips:
    strip = DualStrips(LED_1_COUNT, LED_1_PIN, ... , LED_2_COUNT, LED_2_PIN, ... , reverse_idx=True)
else:
    strip = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, ...)
    
if applyGamma:
    colorMaker = GammaColor()
else:
    colorMaker = OriginColor()
    
strip.begin()
strip.setPixelColor(100, colorMaker.make(128, 128, 128))
strip.show()
```
