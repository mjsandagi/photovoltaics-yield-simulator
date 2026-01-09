"""
This file contains the functions that calculate:
1. The Declination Angle (δ): the tilt of the Earth relative to the Sun (changes with the day of the year).
2. The Solar Elevation Angle (α): the Sun's height above the horizon at Solar Noon.
3. The Angle of Incidence (θ): the multiplier that tells you how much of the GHI actually "hits" the tilted panel surface.
"""
import math

def declination_angle(n):
    inner_radians = math.radians((360 * ((284+n)/365)))
    delta = 23.45 * math.sin(math.radians(inner_radians))
    return delta
