"""
This file contains the functions that calculate solar geometry for daily resolution:
1. The Declination Angle (δ): The tilt of the Earth relative to the Sun.
2. The Sunset Hour Angle (Ωs): The angle representing half the day length.
3. The Geometric Factor (Rb): The ratio of beam radiation on the tilted surface 
   vs. the horizontal surface (integrated over the day).

Assumptions:
- South-facing surface (azimuth = 180°)
- Daily-integrated beam radiation
- No horizon shading
"""
import math

def declination_angle(n):
    """
    Calculates the solar declination angle for a given day of the year.
    The declination angle is the angle between the rays of the sun and the plane of the Earth's equator.

    It varies throughout the year as the Earth orbits the sun.
    Parameters:
        n (int): The day of the year (1 for January 1st, 365 for December 31st).
    Returns:
        float: The declination angle in degrees.
    """

    inner_radians = math.radians((360 * ((284+n)/365)))
    delta = 23.45 * math.sin(inner_radians)
    return delta

def sunset_hour_angle(lat, delta):
    """
    Calculates the Sunset Hour Angle (omega_s) in radians.
    Parameters:
        lat (float): Latitude in degrees
        delta (float): Declination angle in degrees

    Returns:
        float: Sunset hour angle in radians
    """
    lat_rad = math.radians(lat)
    delta_rad = math.radians(delta)
    
    # Calculate cosine of omega_s
    # cos(w_s) = -tan(phi) * tan(delta)
    cos_ws = -math.tan(lat_rad) * math.tan(delta_rad)
    
    # Safety check: ensure value is within -1 to 1 (for polar circles)
    cos_ws = max(-1.0, min(1.0, cos_ws))
    
    return math.acos(cos_ws)

def geometric_factor_rb(lat, tilt, n):
    """
    Calculates the Geometric Factor (Rb) for a south-facing surface.
    This integrates the incidence angle from sunrise to sunset.
    Rb is simply the ratio of daily beam irradiance on a tilted 
    surface to that on a horizontal surface.

    Parameters:
        lat (float): Latitude in degrees
        tilt (float): Panel tilt in degrees
        n (int): Day of the year (1-365)
    Returns:
        float: Rb geometric factor (dimensionless)
    """
    # 1. Get derived geometry variables
    delta = declination_angle(n)
    omega_s = sunset_hour_angle(lat, delta) # in radians
    
    # 2. Convert degrees to radians for the formula
    lat_rad = math.radians(lat)
    delta_rad = math.radians(delta)
    tilt_rad = math.radians(tilt)
    
    # 3. Calculate numerator (Beam on Tilted Surface)
    # Note: For south facing, we replace phi with (phi - tilt)
    numerator = (
        math.cos(lat_rad - tilt_rad) * math.cos(delta_rad) * math.sin(omega_s) +
        omega_s * math.sin(lat_rad - tilt_rad) * math.sin(delta_rad)
    )
    
    # 4. Calculate denominator (Beam on Horizontal Surface)
    denominator = (
        math.cos(lat_rad) * math.cos(delta_rad) * math.sin(omega_s) +
        omega_s * math.sin(lat_rad) * math.sin(delta_rad)
    )
    
    # Avoid division by zero (e.g., polar night)
    if denominator <= 0:
        return 0.0
        
    return numerator / denominator


