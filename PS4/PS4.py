# %% base script
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
from uncertainties import unumpy as unp
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

# Strom bei I_B = 0: -0.8 mV
I = np.array([30, 24, 19, 13, 7, 2]) * 1e-3
UH = -np.array([-38.3, -31.5, -24.5, -16.9, -9.2, -4.1]) * 1e-3
dUH = abs(UH * 0.008) + np.full_like(UH, 3e-4)
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
RH = a * d / -B

# ---------- Ladungsträgerdichte ----------
n = -1 / (e * RH)

# ---------- Ausgabe ----------
print("Steigung =", a)
print("Achsenabschnitt =", b)

print("Hallkonstante RH =", RH * 1e6, "cm^3/C")
print("Ladungsträgerdichte n =", n * 1e-6, "1/cm^3")

# ---------- Plot ----------
xfit = np.linspace(min(I), max(I), 500)

plt.errorbar(
    I * 1e3,
    UH * 1e3,
    yerr=dUH * 1e3,
    fmt="o",
    capsize=4,
    label="Messdaten",
    markersize=5,
)

plt.plot(xfit * 1e3, linear(xfit, *popt) * 1e3, label="Fit: UH = a*I + b")

plt.title("Hallspannung UH gegen Strom I")
plt.xlabel("I [mA]")
plt.ylabel("UH [mV]")
plt.legend()
plt.grid()

plt.show()


# %% Aufgabe 4 n-Dotierung
d = 1e-3  # uncertainty? ANPASSEN!
b_conv = ufloat(48.7, 0.25)  # from A to mT

# bei I_B = 0: U_H = -1.1 mV , U = 0.959 V

# ---------- PlusFeld ----------
B1 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * b_conv.n * 1e-3
UH1 = (
    np.array([-1.1, -5.7, -10.6, -15.8, -20.9, -25.9, -31.0, -35.0, -41.0, -45.4])
    * 1e-3
)
dUH1 = abs(UH1 * 0.008) + np.full_like(UH1, 3e-4)
U1 = np.array([0.959, 0.960, 0.961, 0.962, 0.963, 0.964, 0.966, 0.968, 0.971, 0.973])
dU1 = abs(U1 * 0.005) + np.full_like(U1, 1e-3)
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)

# ---------- MinusFeld ----------
B2 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * -b_conv.n * 1e-3
UH2 = np.array([-1.1, 4.9, 9.5, 14.8, 20.1, 25.4, 30.7, 35.6, 41.2, 44.7]) * 1e-3
dUH2 = abs(UH2 * 0.008) + np.full_like(UH2, 3e-4)
U2 = np.array([0.961, 0.960, 0.960, 0.961, 0.962, 0.964, 0.966, 0.968, 0.970, 0.972])
dU2 = abs(U2 * 0.005) + np.full_like(U2, 1e-3)

# ---------- Kombinieren ----------
B = np.concatenate([B1, B2])
dB = abs(0.02 * B)  # confusion, what about b_conv.s? maybe add it to dB? ANPASSEN!
UH = np.concatenate([UH1, UH2])
dUH = np.concatenate([dUH1, dUH2])
U = np.concatenate([U1, U2])
dU = np.concatenate([dU1, dU2])


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

n = -1 / (e * RH)

print("RH =", RH * 1e6, "cm^3/C")
print("n =", n * 1e-6, "1/cm^3")

# ---------- Plot ----------
xfit = np.linspace(min(B), max(B), 500)

plt.errorbar(
    B1 * 1e3, UH1 * 1e3, yerr=dUH1 * 1e3, capsize=4, fmt="o", label="B positiv"
)
plt.errorbar(
    B2 * 1e3, UH2 * 1e3, yerr=dUH2 * 1e3, capsize=4, fmt="o", label="B negativ"
)

plt.plot(xfit * 1e3, linear(xfit, *popt) * 1e3, label="Fit: UH = a*B + b")

plt.title("Hallspannung UH gegen Magnetfeld B")
plt.xlabel("B [mT]")
plt.ylabel("UH [mV]")
plt.grid()
plt.legend()

plt.show()


# %% Aufgabe 5
l = 20e-3  # Länge der Probe in m
A = 10e-3 * 1e-3  # Querschnittsfläche der Probe in m^2

I = ufloat(25e-3, 0.001e-3)  # Konstantstrom, Fehler anpassen!

n = ufloat((7.57 + 7.467) / 2, 0.15) * 1e20
# ---------- PlusFeld ----------
B1 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * b_conv.n * 1e-3
UH1 = (
    np.array([-1.1, -5.7, -10.6, -15.8, -20.9, -25.9, -31.0, -35.0, -41.0, -45.4])
    * 1e-3
)
dUH1 = abs(UH1 * 0.008) + np.full_like(UH1, 3e-4)
U1 = np.array([0.959, 0.960, 0.961, 0.962, 0.963, 0.964, 0.966, 0.968, 0.971, 0.973])
dU1 = abs(U1 * 0.005) + np.full_like(U1, 1e-3)
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)

# ---------- MinusFeld ----------
B2 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * -b_conv.n * 1e-3
UH2 = np.array([-1.1, 4.9, 9.5, 14.8, 20.1, 25.4, 30.7, 35.6, 41.2, 44.7]) * 1e-3
dUH2 = abs(UH2 * 0.008) + np.full_like(UH2, 3e-4)
U2 = np.array([0.961, 0.960, 0.960, 0.961, 0.962, 0.964, 0.966, 0.968, 0.970, 0.972])
dU2 = abs(U2 * 0.005) + np.full_like(U2, 1e-3)

R1 = U1 / I.n
dR1 = R1 * np.sqrt((dU1 / U1) ** 2 + (I.s / I.n) ** 2)
R2 = U2 / I.n
dR2 = R2 * np.sqrt((dU2 / U2) ** 2 + (I.s / I.n) ** 2)

# ---------- R(0) bestimmen ----------
R1_0 = R1[0]
dR1_0 = dR1[0]
R2_0 = R2[0]
dR2_0 = dR2[0]

# ---------- Magnetwiderstand ----------
deltaR1 = (R1 - R1_0) / R1_0
d_deltaR1 = abs(deltaR1 * np.sqrt((dR1 / R1) ** 2 + (dR1_0 / R1_0) ** 2))
deltaR2 = (R2 - R2_0) / R2_0
d_deltaR2 = abs(deltaR2 * np.sqrt((dR2 / R2) ** 2 + (dR2_0 / R2_0) ** 2))

# ---------- Leitfähigkeit ----------
sigma1 = l / (A * R1_0)
sigma2 = l / (A * R2_0)

print("Leitfähigkeit bei B positiv =", sigma1)
print("Leitfähigkeit bei B negativ =", sigma2)

# ---------- Beweglichkeit ----------
mu1 = sigma1 / (n * e)
mu2 = sigma2 / (n * e)

print("Beweglichkeit bei B positiv =", mu1)
print("Beweglichkeit bei B negativ =", mu2)

# ---------- Plot ----------
plt.errorbar(B1**2, deltaR1, yerr=d_deltaR1, capsize=4, fmt="o", label="B positiv")
plt.errorbar(B2**2, deltaR2, yerr=d_deltaR2, capsize=4, fmt="s", label="B negativ")

plt.xlabel(r"$B^2$ [T$^2$]")
plt.ylabel(r"$\Delta R/R(0)$")

plt.grid()
plt.show()


# %% Aufgabe 6 p-Dotierung
d = 1e-3  # uncertainty? ANPASSEN!
l = 20e-3  # Länge der Probe in m
A = 10e-3 * 1e-3  # Querschnittsfläche der Probe in m^2
b_conv = ufloat(48.7, 0.25)  # from A to mT

# ---------- Plusfeld ----------
B1 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * b_conv.n
UH1 = np.array([-3.8, 1.6, 6.6, 11.7, 16.8, 21.9, 26.8, 31.5, 36.1, 40.4]) * 1e-3
dUH1 = np.full_like(UH1, 1e-4)
U1 = np.array([1.447, 1.447, 1.448, 1.450, 1.452, 1.455, 1.458, 1.461, 1.465, 1.469])
dU1 = np.full_like(U1, 1e-3)
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)

# ---------- Minusfeld ----------
B2 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * -b_conv.n
UH2 = (
    np.array([-3.7, -8.4, -13.0, -18.1, -23.3, -28.0, -32.6, -37.2, -42.0, -45.9])
    * 1e-3
)
dUH2 = np.full_like(UH2, 1e-4)
U2 = np.array([1.443, 1.444, 1.446, 1.447, 1.449, 1.452, 1.455, 1.459, 1.463, 1.467])
dU2 = np.full_like(U2, 1e-3)

# ---------- Kombinieren ----------
B = np.concatenate([B1, B2])
dB = 0.02 * B  # confusion, what about b_conv.s? maybe add it to dB? ANPASSEN!
UH = np.concatenate([UH1, UH2])
dUH = np.concatenate([dUH1, dUH2])
U = np.concatenate([U1, U2])
dU = np.concatenate([dU1, dU2])


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

p = 1 / (e * RH)

print("RH =", RH)
print("p =", p)

# ---------- Plot ----------
xfit = np.linspace(min(B), max(B), 500)

plt.errorbar(B1, UH1, yerr=dUH1, fmt="o", label="B positiv")
plt.errorbar(B2, UH2, yerr=dUH2, fmt="o", label="B negativ")

plt.plot(xfit, linear(xfit, *popt), label="Fit")

plt.xlabel("B [T]")
plt.ylabel("UH [V]")
plt.grid()
plt.legend()

plt.show()


R1 = U1 / I.n
dR1 = R1 * np.sqrt((dU1 / U1) ** 2 + (I.s / I.n) ** 2)
R2 = U2 / I.n
dR2 = R2 * np.sqrt((dU2 / U2) ** 2 + (I.s / I.n) ** 2)

# ---------- R(0) bestimmen ----------
R1_0 = R1[0]
dR1_0 = dR1[0]
R2_0 = R2[0]
dR2_0 = dR2[0]

# ---------- Magnetwiderstand ----------
deltaR1 = (R1 - R1_0) / R1_0
d_deltaR1 = deltaR1 * np.sqrt((dR1 / R1) ** 2 + (dR1_0 / R1_0) ** 2)
deltaR2 = (R2 - R2_0) / R2_0
d_deltaR2 = deltaR2 * np.sqrt((dR2 / R2) ** 2 + (dR2_0 / R2_0) ** 2)

# ---------- Leitfähigkeit ----------
sigma1 = l / (A * R1_0)
sigma2 = l / (A * R2_0)

print("Leitfähigkeit bei B positiv =", sigma1)
print("Leitfähigkeit bei B negativ =", sigma2)

# ---------- Beweglichkeit ----------
mu1 = sigma1 / (p * e)
mu2 = sigma2 / (p * e)

print("Beweglichkeit bei B positiv =", mu1)
print("Beweglichkeit bei B negativ =", mu2)

# ---------- Plot ----------
plt.errorbar(B1**2, deltaR1, yerr=d_deltaR1, fmt="o", label="B positiv")
plt.errorbar(B2**2, deltaR2, yerr=d_deltaR2, fmt="s", label="B negativ")

plt.xlabel(r"$B^2$ [T$^2$]")
plt.ylabel(r"$(R(B)-R(0))/R(0)$")

plt.grid()
plt.show()


# %% Aufgabe 7
# ---------- Konstantstrom ----------
I = ufloat(25e-3, 0.001e-3)

# Endwert von I_B = 3.894 A
# Fehler anpassen!

# ---------- Daten laden ----------
data = pd.read_csv("Di09_PS4.csv", delimiter=",", decimal=".")

# ---------- Spaltennamen anpassen ----------
T = data["Temperatur"].to_numpy()

UH = data["Hallspannung"].to_numpy()
U = data["Längsspannung"].to_numpy()

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

# %%
