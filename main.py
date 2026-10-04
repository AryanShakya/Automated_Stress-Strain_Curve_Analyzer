import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

length = 20.12 # mm
area = 96.7 # mm^2

df = pd.read_excel('dataset.xlsx') # Creates the dataframe

#Creating New Columns
df["Stress (GPa)"] = df["Load (kN)"]/area # Creates Stress column by formula F/A
df["Strain"] = df["Extension (mm)"]/length # Creates Strain column by fromula Extension/original length

# Dropping Additional columns
df = df[['Stress (GPa)', 'Strain']]

# Calculating Young's Modulus

uts = df['Stress (GPa)'].max() # Gets uts, by taking maximum value of stress
uts_id = df['Stress (GPa)'].idxmax() # Gives index of max value cell
strain_uts = df['Strain'].loc[df.index[uts_id]] # Gets Strain corresponding to uts

upper_lim = uts * .3 # These are upper and lower limits in which elastic zone will be present
lower_lim = uts * .1

slice_df = df.loc[(df['Stress (GPa)'] > lower_lim) & (df['Stress (GPa)'] < upper_lim) ] # Slices and creates a new dataframe for the elastic region

coeff = np.polyfit(slice_df['Strain'], slice_df['Stress (GPa)'], 1) # Gives coefficients of linear polynomial fitted for slice_df dataframe

young_mod = coeff[0] # Young's Modulus
intercept = coeff[1] # Intercept of polynomial

# Calculating Yield Strength

df["Offset Stress"] = young_mod * (df["Strain"] - .002) + intercept # Calculating Offset Stress

df["Physical Stress - Theoretical Stress"] = df["Stress (GPa)"] - df["Offset Stress"] # Calculating difference between theoretical and physical stress

neg_df = df.loc[ df['Physical Stress - Theoretical Stress'] < 0 ] # Creates a dataframe including all the negative values of column Physical Stress - Theoretical Stress

yield_strength = neg_df['Stress (GPa)'].loc[neg_df.index[0]] # Getting the Stress of the first row of Stress (GPa) column
strain_yield_strength = df['Strain'].loc[neg_df.index[0]] # Gets Strain corresponding to Yield Strength

# Calculating Fracture Point

frac_point_stress = df['Stress (GPa)'].iloc[-1]
frac_point_strain = df['Strain'].iloc[-1]

# Creating Graph

# Plotting
plt.plot(df['Strain'], df['Stress (GPa)'],marker='o', linestyle=':', color='purple') # Plots the main graph
# plt.plot(slice_df['Strain'], slice_df['Stress (GPa)'],marker='o', linestyle=':', color='blue') # Plots the elastic region in which we are calculating our young's modulus
plt.plot(strain_uts, uts,marker='o', color='orange') # Plots the Ultimate Tensile Strength
plt.plot(strain_yield_strength, yield_strength,marker='o', color='lightgreen') # Plots the Yield Strength
plt.plot(frac_point_strain, frac_point_stress,marker='o', color='red') # Plots the Fracture Point

# Adding Annotation
plt.annotate('Ultimate Tensile Strength', xy=(strain_uts, uts), xytext=(strain_uts, uts * .5), arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate('Yield Strength', xy=(strain_yield_strength, yield_strength), xytext=(strain_yield_strength * 2 , yield_strength), arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate('Fracture Point', xy=(frac_point_strain, frac_point_stress), xytext=(frac_point_strain * .5 , frac_point_strain * .5), arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.xlabel("Strain")
plt.ylabel("Stress (GPa)")
plt.title("Stress (GPa) vs Strain")
plt.show()

