# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- Konstanten ---
k = 1.380649e-23  # Boltzmann-Konstante
q = 1.602176634e-19  # Elementarladung
T = 300  # Temperatur in Kelvin (anpassen wenn nötig)
U_T = k * T / q  # thermische Spannung


# --- Shockley-Funktion ---
def shockley(U, I_s, n):
    return I_s * (np.exp(U / (n * U_T)) - 1)


# --- Daten einlesen ---
# CSV mit ; als Separator und , als Dezimaltrennzeichen
file_path = "diode_data.csv"

data = pd.read_csv(file_path, sep=";", decimal=",")

# Spaltennamen ggf. anpassen!
U = data.iloc[:, 0].values  # Spannung
I = data.iloc[:, 1].values  # Strom

# --- Fitbereich wählen (optional, wichtig!) ---
# Nur Vorwärtsrichtung (z.B. U > 0.1 V)
mask = U > 0.1
U_fit = U[mask]
I_fit = I[mask]

# --- Fit ---
initial_guess = [1e-12, 1.5]  # Startwerte für I_s und n

params, covariance = curve_fit(shockley, U_fit, I_fit, p0=initial_guess)

I_s_fit, n_fit = params

print(f"I_s = {I_s_fit:.3e} A")
print(f"n   = {n_fit:.3f}")

# --- Plot ---
U_plot = np.linspace(min(U_fit), max(U_fit), 300)
I_plot = shockley(U_plot, I_s_fit, n_fit)

plt.figure()
plt.scatter(U, I, label="Messdaten", s=10)
plt.plot(U_plot, I_plot, label="Fit", color="red")
plt.xlabel("Spannung (V)")
plt.ylabel("Strom (A)")
plt.yscale("log")  # sehr sinnvoll bei Dioden!
plt.legend()
plt.grid()

plt.show()


# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# --- Daten einlesen ---
file_path = "transistor_data.txt"

data = pd.read_csv(file_path, sep=";", decimal=",")

# Spalten anpassen!
I_B = data.iloc[:, 0].values  # Basisstrom
I_C = data.iloc[:, 1].values  # Kollektorstrom

# --- Linearen Bereich wählen ---
# Hier musst du evtl. rumspielen!
mask = (I_B > 1e-6) & (I_B < 1e-4)

I_B_fit = I_B[mask]
I_C_fit = I_C[mask]

# --- Linearer Fit ---
slope, intercept, r_value, p_value, std_err = linregress(I_B_fit, I_C_fit)

beta = slope

print(f"Beta (Verstärkung) = {beta:.2f}")
print(f"Intercept = {intercept:.3e}")
print(f"R^2 = {r_value**2:.4f}")

# --- Plot ---
plt.figure()
plt.scatter(I_B, I_C, label="Messdaten", s=10)
plt.plot(I_B_fit, slope * I_B_fit + intercept, color="red", label="Fit")
plt.xlabel("Basisstrom I_B (A)")
plt.ylabel("Kollektorstrom I_C (A)")
plt.legend()
plt.grid()

plt.show()
