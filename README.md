# Automated Stress-Strain Curve Analyzer

An automated Python tool designed to calculate primary mechanical properties—Young's Modulus, Yield Strength, Ultimate Tensile Strength (UTS), and Fracture Point—from raw universal testing machine (UTM) data. The script processes raw load and displacement measurements, applies statistical regression to isolate elastic behavior, and outputs an annotated stress-strain curve.

## Overview

Manual calculation of tensile properties from raw machine output can be prone to operator error and inconsistencies in selecting the elastic region. This script standardizes the process by:

1. Converting raw force and displacement measurements into engineering stress and strain.
2. Automatically filtering out machine settling (toe region) and plastic non-linearities.
3. Calculating Young's Modulus using Ordinary Least Squares (OLS) linear regression.
4. Applying a standard 0.2% strain offset to locate Yield Strength.
5. Plotting a labeled visualization highlighting critical material thresholds.

## Features

- **Data Transformation**: Converts raw load ($\text{kN}$) and extension ($\text{mm}$) into engineering stress ($\text{GPa}$) and strain ($\text{mm/mm}$)[cite: 9].
- **Elastic Region Slicing**: Filters stress values between 10% and 30% of UTS to isolate the linear elastic range, eliminating machine slack and onset yielding from regression calculations[cite: 9].
- **Linear Fit Regression**: Fits a first-degree polynomial (`numpy.polyfit`) to extract slope (Young's Modulus, $E$) and y-intercept ($c$)[cite: 9].
- **0.2% Offset Yield Identification**: Constructs the offset line equation and determines the zero-crossing point where physical curve data intersects the offset line[cite: 9].
- **Critical Point Extraction**: Identifies UTS (peak stress) and Fracture Point (final dataset coordinate)[cite: 9].
- **Graphical Visualization**: Uses Matplotlib to plot the full stress-strain curve alongside marked landmarks and arrow annotations[cite: 9].

## Mathematical Method

### 1. Engineering Stress and Strain Conversion
$$\text{Stress } (\sigma) = \frac{\text{Load } (F)}{\text{Cross-Sectional Area } (A_0)} \quad [\text{GPa}]$$

$$\text{Strain } (\epsilon) = \frac{\text{Extension } (\Delta L)}{\text{Original Gauge Length } (L_0)}$$

### 2. Young's Modulus ($E$)
Determined via OLS linear regression across the filtered elastic subset ($0.10 \cdot \sigma_{\text{UTS}} \le \sigma \le 0.30 \cdot \sigma_{\text{UTS}}$)[cite: 9]:
$$\sigma = E \cdot \epsilon + c$$

### 3. Yield Strength ($0.2\%$ Offset)
Calculated by shifting the linear elastic fit right by $0.002$ strain[cite: 9]:
$$\sigma_{\text{offset}} = E \cdot (\epsilon - 0.002) + c$$

Yield strength corresponds to the first data index where physical stress drops below theoretical offset stress[cite: 9]:
$$\sigma_{\text{physical}} - \sigma_{\text{offset}} < 0$$

## Repository Structure

```text
├── dataset.xlsx       # Excel file containing raw tensile test data
├── main_2.py          # Primary analytical script
├── requirements.txt   # Python environment dependencies
└── README.md          # Project documentation
