# %% base script
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
from uncertainties.umath import *
import pandas as pd

# ---------- Konstanten ----------
e = 1.602176634e-19  # Elementarladung in C


# ---------- Linearfunktion ----------
def linear(x, a, b):
    return a * x + b


# ---------- Linearer Fit ----------
def linear_fit(x, y, dy):
    popt, pcov = curve_fit(linear, x, y, sigma=dy, absolute_sigma=True)

    a, b = popt
    da, db = np.sqrt(np.diag(pcov))

    return (ufloat(a, da), ufloat(b, db))


# %% Aufgabe 1
# ---------- Parameter ----------
B = ufloat(150e-3, 0.02 * 150e-3)  # Unsicherheit anpassen!
d = 1e-3  # Probendicke in m (maybe uncertainties? ANPASSEN!)

# ---------- Daten laden ----------
data = pd.read_csv("aufgabe1.csv")

I = data["I_mA"].to_numpy() * 1e-3
UH = data["UH_mV"].to_numpy() * 1e-3
dUH = data["dUH_mV"].to_numpy() * 1e-3
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)


# ---------- Fitfunktion ----------
def linear(x, a, b):
    return a * x + b


# ---------- Fit ----------
popt, pcov = curve_fit(linear, I, UH, sigma=dUH, absolute_sigma=True)

a, b = popt
da, db = np.sqrt(np.diag(pcov))

a = ufloat(a, da)
b = ufloat(b, db)

# ---------- Hallkonstante ----------
RH = a * d / B

# ---------- Ladungsträgerdichte ----------
n = 1 / (e * RH)

# ---------- Ausgabe ----------
print("Steigung =", a)
print("Achsenabschnitt =", b)

print("Hallkonstante RH =", RH, "m^3/C")
print("Ladungsträgerdichte n =", n, "1/m^3")

# ---------- Plot ----------
xfit = np.linspace(min(I), max(I), 500)

plt.errorbar(I, UH, yerr=dUH, fmt="o", capsize=3, label="Messdaten")

plt.plot(xfit, linear(xfit, *popt), label="Linearer Fit")

plt.xlabel("I [A]")
plt.ylabel("UH [V]")
plt.legend()
plt.grid()

plt.show()


# %% Aufgabe 4
d = 1e-3  # anpassen

# ---------- Daten ----------
data1 = pd.read_csv("feld_plus.csv")
data2 = pd.read_csv("feld_minus.csv")

# ---------- Plusfeld ----------
B1 = data1["B_mT"].to_numpy() * 1e-3
UH1 = data1["UH_mV"].to_numpy() * 1e-3
dUH1 = data1["dUH_mV"].to_numpy() * 1e-3
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)

# ---------- Minusfeld ----------
B2 = -data2["B_mT"].to_numpy() * 1e-3
UH2 = data2["UH_mV"].to_numpy() * 1e-3
dUH2 = data2["dUH_mV"].to_numpy() * 1e-3

# ---------- Kombinieren ----------
B = np.concatenate([B1, B2])
dB = 0.02 * B
UH = np.concatenate([UH1, UH2])
dUH = np.concatenate([dUH1, dUH2])


# ---------- Fit ----------
def linear(x, a, b):
    return a * x + b


popt, pcov = curve_fit(linear, B, UH, sigma=dUH, absolute_sigma=True)

a, b = popt
da, db = np.sqrt(np.diag(pcov))

a = ufloat(a, da)

# ---------- Hallkonstante ----------
I = ufloat(25e-3, 0.001e-3)  # Konstantstrom, Fehler anpassen!

RH = a * d / I

n = 1 / (e * RH)
# maybe add error to n?

print("RH =", RH)
print("n =", n)

# ---------- Plot ----------
xfit = np.linspace(min(B), max(B), 500)

plt.errorbar(B1, UH1, xerr=dB, yerr=dUH1, fmt="o", label="B positiv")
plt.errorbar(B2, UH2, xerr=dB, yerr=dUH2, fmt="o", label="B negativ")

plt.plot(xfit, linear(xfit, *popt), label="Fit")

plt.xlabel("B [T]")
plt.ylabel("UH [V]")
plt.grid()
plt.legend()

plt.show()


# %% Aufgabe 5
I = ufloat(25e-3, 0.001e-3)  # Konstantstrom, Fehler anpassen!

data = pd.read_csv("feld_plus.csv")

B = data["B_mT"].to_numpy() * 1e-3
U = data["U_mV"].to_numpy() * 1e-3

R = U / I

# ---------- R(0) bestimmen ----------
idx0 = np.argmin(np.abs(B))
R0 = R[idx0]

# ---------- Magnetwiderstand ----------
deltaR = (R - R0) / R0

# ---------- Plot ----------
plt.plot(B**2, deltaR, "o")

plt.xlabel(r"$B^2$ [T$^2$]")
plt.ylabel(r"$(R(B)-R(0))/R(0)$")

plt.grid()
plt.show()


# %% Aufgabe 6
# ---------- Konstantstrom ----------
I = ufloat(25e-3, 0.001e-3)
# Fehler anpassen!

# ---------- Daten laden ----------
data = pd.read_csv("temperatur.csv")

# ---------- Spaltennamen anpassen ----------
T = data["Temperatur"].to_numpy()

UH = data["UH"].to_numpy()
U = data["U"].to_numpy()

# ---------- Spannungsfehler ----------
dUH = np.full_like(UH, 0.001)
dU = np.full_like(U, 0.001)

# ---------- Widerstand ----------
R = U / I.n

# ---------- Fehler von R ----------
dR = R * np.sqrt((dU / U) ** 2 + (I.s / I.n) ** 2)

# ---------- UH(T) ----------
plt.figure()

plt.errorbar(T, UH, yerr=dUH, fmt="o", capsize=3)

plt.xlabel("Temperatur [°C]")
plt.ylabel("UH [V]")

plt.grid()

# ---------- U(T) ----------
plt.figure()

plt.errorbar(T, U, yerr=dU, fmt="o", capsize=3)

plt.xlabel("Temperatur [°C]")
plt.ylabel("U [V]")

plt.grid()

# ---------- R(T) ----------
plt.figure()

plt.errorbar(T, R, yerr=dR, fmt="o", capsize=3)

plt.xlabel("Temperatur [°C]")
plt.ylabel("R [Ohm]")

plt.grid()

plt.show()
