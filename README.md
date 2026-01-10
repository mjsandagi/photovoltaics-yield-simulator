# Photovoltaics Yield Simulator

_A physics-inspired photovoltaic energy model_

## Overview

This project implements a **minimal, physics-based photovoltaic (PV) yield simulator** to estimate the daily and annual energy production of a silicon solar cell photovoltaic system.

Rather than relying on machine learning, the model is built directly from **first-principles equations** commonly used in solar engineering, with a particular focus on **quantifying temperature-related efficiency losses**.

The core question this project answers is:

> **How much energy yield do we overestimate if we ignore temperature effects in photovoltaic modelling?**

---

## Motivation

Many introductory photovoltaic models assume constant panel efficiency, which can lead to **systematic overestimation of energy yield**, particularly during warmer months.

This project compares:

-   A baseline **ideal PV model** (no losses)
-   A **temperature-adjusted PV model** incorporating cell temperature effects

By isolating temperature losses, the simulator highlights:

-   Daily yield differences
-   Seasonal trends
-   Annual energy loss due to temperature alone

The goal is not maximal realism, but **clarity, interpretability, and engineering insight**.

---

## Model Assumptions

To keep the model focused and interpretable, the following assumptions are made:

-   No shading or horizon obstruction
-   No inverter, wiring, or soiling losses
-   Fixed-tilt PV system
-   Isotropic diffuse irradiance model
-   Single representative temperature coefficient (typical crystalline silicon)

These simplifications allow temperature effects to be studied in isolation.

---

## Model Formulation

### 1. Solar Irradiance

Global Horizontal Irradiance (GHI) is converted to **plane-of-array (POA) irradiance** using a simplified transposition model that accounts for panel tilt and orientation.

---

### 2. Ideal PV Energy Model

The ideal energy yield assumes constant panel efficiency:

`E_ideal = G_POA × P_rated`

This serves as a **control model** against which losses are measured.

---

### 3. Temperature-Adjusted Model

Cell temperature is estimated using a standard Nominal Operating Cell Temperature-based formulation:

`T_cell = T_ambient + ((NOCT - 20)/800) × G_POA`


Efficiency is adjusted using a linear temperature coefficient:

`η(T) = η_ref * (1 + γ * (T_cell - 25))`


The resulting energy yield is computed as:

`E_temp = G_POA × η(T)`


---

## Results

The simulator produces:

-   Daily energy yield curves (ideal vs temperature-adjusted)
-   Monthly and annual energy totals
-   Percentage energy loss attributable solely to temperature effects

Across a typical year, the temperature-adjusted model predicts an **annual energy reduction of approximately X–Y%**, with losses peaking during summer months.

_(Exact values depend on location and system configuration.)_

---

## Usage

### Command Line Interface

```bash
python cli.py \
  --lat 51.5 \
  --lon -0.1 \
  --tilt 30 \
  --azimuth 180 \
  --capacity 4.0
```

### Example Output

```text
Annual Yield (Ideal): 4,120 kWh
Annual Yield (Temp-Adjusted): 3,760 kWh
Temperature Loss: 8.7%
```

---

## Project Structure

```text
photovoltaics-yield-simulator/
├── solar_geometry.py
├── irradiance.py
├── temperature.py
├── pv_model.py
├── notebooks/
│   └── data_exploration.ipynb
├── data/
│   └── weather_london_2023.csv
│   └── weather_london_2023_cleaned.csv
├── cli.py
├── plots.py
└── README.md
```

## Future Extensions

-   Hourly time-step simulation
-   Degradation modelling
-   Battery-coupled systems
-   Validation against real PV system data
-   Modelling of shading and degradation
-   Advanced irradiance transposition model
