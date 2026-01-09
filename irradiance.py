"""
This module computes daily plane-of-array (POA) irradiance
from daily global horizontal irradiance (GHI).

Assumptions:
- Fixed, south-facing surface
- Daily-integrated irradiance
- Isotropic diffuse radiation model
- Constant beam/diffuse split
"""

import math
import solar_geometry

def poa_irradiance_daily(ghi, lat, tilt, day_of_year, beam_fraction=0.7):
    """
    Computes daily plane-of-array (POA) irradiance.

    Parameters:
        ghi (float): Global Horizontal Irradiance [kWh/m^2/day]
        lat (float): Latitude [degrees]
        tilt (float): Panel tilt angle [degrees]
        day_of_year (int): Day of year (1-365)
        beam_fraction (float): Fraction of GHI assumed to be beam radiation

    Returns:
        float: POA irradiance [kWh/m^2/day]
    """
    if ghi <= 0:
        return 0.0
    beam_fraction = max(0.0, min(1.0, beam_fraction))
    diffuse_fraction = 1.0 - beam_fraction

    # Split GHI
    Hb = beam_fraction * ghi
    Hd = diffuse_fraction * ghi

    # Geometric factor for beam radiation
    Rb = solar_geometry.geometric_factor_rb(lat, tilt, day_of_year)

    # Beam component on tilted surface
    Hb_tilted = Hb * Rb

    # Diffuse component (isotropic sky model)
    tilt_rad = math.radians(tilt)
    Hd_tilted = Hd * (1 + math.cos(tilt_rad)) / 2

    # Total POA irradiance
    G_poa = Hb_tilted + Hd_tilted

    return G_poa

