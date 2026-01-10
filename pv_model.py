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

def pv_energy_temp_adjusted_daily(ghi, temp_air, lat, tilt, day_of_year, capacity_kwp, gamma=-0.004, noct=45):
    """
    Calculates the daily photovoltaic (PV) energy output adjusted for cell temperature effects using the NOCT (Nominal Operating Cell Temperature) model.
    This function estimates the PV cell temperature based on the NOCT model:
        T_cell = T_air + ((NOCT - 20) / 800) * G_poa
    where:
        - T_cell: PV cell temperature in degrees Celsius
        - T_air: Ambient air temperature in degrees Celsius
        - NOCT: Nominal Operating Cell Temperature (default 45°C)
        - G_poa: Plane-of-array irradiance in W/m² (averaged over the day)
    A temperature correction factor (ft) is then applied to the ideal energy output to account for the effect of cell temperature on PV efficiency:
        ft = 1 + gamma * (T_cell - 25)
    where:
        - gamma: Temperature coefficient (default -0.004 per °C)
        - 25°C: Reference cell temperature
    Parameters:
        ghi (float): Daily global horizontal irradiance (kWh/m²).
        temp_air (float): Daily average ambient air temperature (°C).
        lat (float): Latitude of the location (degrees).
        tilt (float): Tilt angle of the PV array (degrees).
        day_of_year (int): Day of the year (1-366).
        capacity_kwp (float): Installed PV system capacity (kWp).
        gamma (float, optional): Temperature coefficient of power (%/°C, default -0.004).
        noct (float, optional): Nominal Operating Cell Temperature (°C, default 45).
    Returns:
        float: Temperature-adjusted daily PV energy output (kWh).
    Notes:
        - The function assumes the use of the NOCT model for cell temperature estimation.
        - All energy values are in kWh, irradiance in kWh/m², temperatures in °C, and capacity in kWp.
    """
    # G_poa is approximated as a daily-average irradiance.
    Gpoa_avg = (irrad.poa_irradiance_daily(ghi, lat, tilt, day_of_year) * 1000)/6
    fragment = ((noct - 20)/800) * Gpoa_avg
    temp_cell = temp_air + fragment

    # Temperature Correction Factor
    ft = 1 + (gamma * (temp_cell - 25))
    ft = max(ft, 0) # Clamp the TCF to avoid pathological cases.
    Eideal = ideal_daily_photovoltaic_energy_output(ghi, lat, tilt, day_of_year, capacity_kwp)
    Etemp = Eideal * ft
    return Etemp