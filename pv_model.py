"""
Note that kWp = power output at 1000W/m^2 irradiance and 25°C
"""
import irradiance as irrad

def ideal_daily_photovoltaic_energy_output(
    ghi,
    lat,
    tilt,
    day_of_year,
    capacity_kwp
):
    """
    Computes ideal daily PV energy yield (no temperature losses).

    Parameters:
        ghi (float): Global Horizontal Irradiance [kWh/m^2/day]
        lat (float): Latitude [degrees]
        tilt (float): Panel tilt angle [degrees]
        day_of_year (int): Day of year (1-365)
        capacity_kwp (float): System rated power [kWp]

    Returns:
        float: Ideal daily energy yield [kWh/day]
    """
    irradiance = irrad.poa_irradiance_daily(ghi, lat, tilt, day_of_year)
    Eideal = irradiance * capacity_kwp
    return Eideal
