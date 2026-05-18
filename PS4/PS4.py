# %% base script
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
from uncertaintier import unumpy as unp
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


I = np.array([,]) * 1e-3
UH = np.array([,]) 
dUH = np.array([,])
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
n = -1 / (e * RH)

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


# %% Aufgabe 4 n-Dotierung
d = 1e-3  # uncertainty? ANPASSEN!
b_conv = ufloat(48.7, 0.25) # from A to mT

# ---------- Plusfeld ----------
B1 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * b_conv.n
UH1 = np.array([,]) 
dUH1 = np.array([,])
U1 = np.array([,])
dU1 = np.array([,])
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)

# ---------- Minusfeld ----------
B2 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * - b_conv.n
UH2 = np.array([,]) 
dUH2 = np.array([,])
U2 = np.array([,])
dU2 = np.array([,])

# ---------- Kombinieren ----------
B = np.concatenate([B1, B2])
dB = 0.02 * B                           # confusion, what about b_conv.s? maybe add it to dB? ANPASSEN!
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
l = 20e-3  # Länge der Probe in m
A = 10e-3 * 1e-3  # Querschnittsfläche der Probe in m^2

I = ufloat(25e-3, 0.001e-3)  # Konstantstrom, Fehler anpassen!

# copy n from Aufgabe 4
# copy data from Aufgabe 4 here, but only B, dB, U, dU but not concatenate, because we need to calculate R for each B separately

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
mu1 = sigma1 / (n * e)
mu2 = sigma2 / (n * e)

print("Beweglichkeit bei B positiv =", mu1)
print("Beweglichkeit bei B negativ =", mu2)

# ---------- Plot ----------
plt.errorbar(B1**2, deltaR1, yerr=d_deltaR1, fmt="o", label="B positiv")
plt.errorbar(B2**2, deltaR2, yerr=d_deltaR2, fmt="s", label="B negativ")

plt.xlabel(r"$B^2$ [T$^2$]")
plt.ylabel(r"$(R(B)-R(0))/R(0)$")

plt.grid()
plt.show()


# %% Aufgabe 6 p-Dotierung
d = 1e-3  # uncertainty? ANPASSEN!
l = 20e-3  # Länge der Probe in m
A = 10e-3 * 1e-3  # Querschnittsfläche der Probe in m^2
b_conv = ufloat(48.7, 0.25) # from A to mT

# ---------- Plusfeld ----------
B1 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * b_conv.n
UH1 = np.array([,]) 
dUH1 = np.array([,])
U1 = np.array([,])
dU1 = np.array([,])
# dUH = np.full_like(UH, 1e-3) bzw dUH = 0.01 * UH oder kombo aus beiden Fehlern (ANPASSEN!)

# ---------- Minusfeld ----------
B2 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) * - b_conv.n
UH2 = np.array([,]) 
dUH2 = np.array([,])
U2 = np.array([,])
dU2 = np.array([,])

# ---------- Kombinieren ----------
B = np.concatenate([B1, B2])
dB = 0.02 * B                           # confusion, what about b_conv.s? maybe add it to dB? ANPASSEN!
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

plt.errorbar(B1, UH1, xerr=dB, yerr=dUH1, fmt="o", label="B positiv")
plt.errorbar(B2, UH2, xerr=dB, yerr=dUH2, fmt="o", label="B negativ")

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
# Fehler anpassen!

# ---------- Daten laden ----------
data = pd.read_csv("temperatur.csv", delimiter=",", decimal=".")  

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
