# %%
import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp
import pandas as pd
import matplotlib.pyplot as plt

# 1. Auflösungsvermögen eines Gitters

lamda1 = ufloat(576.96, 0.005)
lamda2 = ufloat(579.07, 0.005)

A = lamda1 / (lamda2 - lamda1)

print(f"A = {A}")

n = np.array([1, 2, 3, 1, 2, 3])  # zuerst links dann rechts
Bwerte = np.array([3, 1.27, 1.04, 2.55, 1.09, 0.77])
dB = 0.05
B = unp.uarray(Bwerte, dB)
g = (n * B) / A  # N = B/G    A = nN mit N = B/g -> g = (nB)/A

g_values = unp.nominal_values(g)
std = np.std(g_values, ddof=1)
error = std / np.sqrt(len(g_values))
g_mean = sum(g) / len(g)

print(f"g_mean \pm Typ-B = {g_mean}")
print(f"Typ-A von g_mean = {error}")
print(g)


# 3. Interferometer

# 1.Datensatz: Interferometer1.csv 23.4 - 29.1
# -----------------------------
# 1. CSV-Datei laden
# -----------------------------
filename = "Interferometer.csv"  # Pfad zur CSV-Datei anpassen
df = pd.read_csv(filename)

# -----------------------------
# 2. Spalten manuell eintragen
# -----------------------------
time_col = "Time since start of measurement"  # Spaltenname für Zeit in CSV
voltage_col = "Voltage"  # Spaltenname für Spannung in CSV
x_error_col = None  # Spaltenname für Unsicherheit Zeit, falls vorhanden
y_error_col = None  # Spaltenname für Spannungsunsicherheit, falls vorhanden

# Falls Fehler-Spalten nicht existieren, kann man auch feste Werte eintragen
# z.B.: y_error = 0.5 mV für alle Messpunkte
# df['y_error'] = 0.5

# -----------------------------
# 3. Daten vorbereiten
# -----------------------------
x = df[time_col]
y = df[voltage_col]

if x_error_col is not None:
    x_err = df[x_error_col]
else:
    x_err = None

if y_error_col is not None:
    y_err = df[y_error_col]
else:
    y_err = None

# -----------------------------
# 4. Plot mit Errorbars
# -----------------------------
plt.figure(figsize=(15, 5))
plt.errorbar(
    x,
    y,
    xerr=x_err,
    yerr=y_err,
    linewidth=1,
    ecolor="red",
    elinewidth=1,
    capsize=2,
    markersize=3,
)
plt.xlabel("Zeit (s)")
plt.ylabel("Spannung (mV)")
plt.title("Michelson Interferometer: Interferenzspannung über Zeit")
plt.grid(True)
plt.tight_layout()
plt.axvline(
    x=27, linestyle="-", linewidth=1, color="green", label=f"Beginn Heizvorgang"
)
plt.axvline(x=257, linestyle="-", linewidth=1, color="red", label=f"Ende Heizvorgang")
plt.legend()
plt.savefig("Michelson Falsch.png")
# -----------------------------
# 5. Plot anzeigen
# -----------------------------
plt.show()


N = ufloat(28 * 2, 1)
lamda = ufloat(632.8, 0.1) * 10 ** (-9)
l_0 = ufloat(89.9, 0.1) * 10 ** (-3)
T_1 = ufloat(296.55, 1.3)
T_2 = ufloat(302.25, 1.3)
T_diff = T_2 - T_1

a = (N * lamda) / (4 * l_0 * T_diff)
print(T_diff)
print(f"{a:.3u}")


# %%
import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp
import pandas as pd
import matplotlib.pyplot as plt


# 3. Interferometer

# 1.Datensatz: Interferometer1.csv 23.4 - 29.1
# -----------------------------
# 1. CSV-Datei laden
# -----------------------------
filename = "Interferometer.csv"  # Pfad zur CSV-Datei anpassen
df = pd.read_csv(filename)

# -----------------------------
# 2. Spalten manuell eintragen
# -----------------------------
time_col = "Time since start of measurement"  # Spaltenname für Zeit in CSV
voltage_col = "Voltage"  # Spaltenname für Spannung in CSV
x_error_col = None  # Spaltenname für Unsicherheit Zeit, falls vorhanden
y_error_col = None  # Spaltenname für Spannungsunsicherheit, falls vorhanden

# Falls Fehler-Spalten nicht existieren, kann man auch feste Werte eintragen
# z.B.: y_error = 0.5 mV für alle Messpunkte
# df['y_error'] = 0.5

# -----------------------------
# 3. Daten vorbereiten
# -----------------------------
x = df[time_col]
y = df[voltage_col]

if x_error_col is not None:
    x_err = df[x_error_col]
else:
    x_err = None

if y_error_col is not None:
    y_err = df[y_error_col]
else:
    y_err = 0.19

# -----------------------------
# 4. Plot mit Errorbars
# -----------------------------
plt.figure(figsize=(15, 5))
plt.errorbar(
    x,
    y,
    xerr=x_err,
    yerr=y_err,
    fmt="o",
    ecolor="grey",
    linewidth=0.5,
    capsize=2,
    markersize=3,
)
plt.xlabel("Zeit (s)")
plt.ylabel("Spannung (mV)")
plt.title("Michelson Interferometer: Interferenzspannung über Zeit")
plt.grid(True)
plt.tight_layout()
plt.axvline(
    x=27, linestyle="-", linewidth=1, color="green", label=f"Beginn Heizvorgang"
)
plt.axvline(x=257, linestyle="-", linewidth=1, color="red", label=f"Ende Heizvorgang")
plt.legend()
plt.savefig("Michelson Punkte.png")
# -----------------------------
# 5. Plot anzeigen
# -----------------------------
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt

filename = "Transmission Farbglasfilter K-5.txt"
header_lines = 24  # 13

data = np.loadtxt(
    filename,
    skiprows=header_lines,
    delimiter="\t",
    converters={
        0: lambda s: float(s.replace(b",", b".")),
        1: lambda s: float(s.replace(b",", b".")),
    },
)

wavelength = data[:, 0]
intensity = data[:, 1]

plt.figure(figsize=(8, 5))

plt.plot(wavelength, intensity)

plt.xlabel("Wellenlänge (nm)")
plt.ylabel("Intensität <%>")
plt.title("Transmission des Farbglasfilters K-5")

plt.axvline(
    x=600, linestyle="--", linewidth=1, color="red", label=f"CW = 601 nm"
)  # 601 61.6
plt.axvline(
    x=853, linestyle="--", linewidth=1, color="red", label=f"CW = 853 nm"
)  # 853 64.8

plt.tight_layout()
plt.legend()
plt.savefig("Transmission Farbglas.png")
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt

filename = "Transmission grüner Interferenzfilter.txt"
header_lines = 24  # 13

data = np.loadtxt(
    filename,
    skiprows=header_lines,
    delimiter="\t",
    converters={
        0: lambda s: float(s.replace(b",", b".")),
        1: lambda s: float(s.replace(b",", b".")),
    },
)

wavelength = data[:, 0]
intensity = data[:, 1]

plt.figure(figsize=(8, 5))

plt.plot(wavelength, intensity)

plt.xlabel("Wellenlänge (nm)")
plt.ylabel("Intensität <%>")
plt.title("Transmission des grünen Interferenzfilters")

# Referenzlinie bei 543 nm
plt.axvline(x=541, linestyle="--", linewidth=1, color="red", label=f"CW = 541 nm")
plt.axvline(
    x=546.0843,
    linestyle="--",
    linewidth=0.5,
    color="black",
    label=f"lower FWHM bound = 536.6 nm",
)  # 546.8
plt.axvline(
    x=536.3,
    linestyle="--",
    linewidth=0.5,
    color="black",
    label=f"upper FWHM bound = 546.8 nm",
)  # 536.6
# plt.text(543, max(intensity)*0.9, "CW 541")
plt.axhline(
    y=27.7, linestyle="--", linewidth=1, color="green", label="FWHM at 27.7 % Intensity"
)

plt.tight_layout()
plt.legend()
plt.savefig("Transmission Interferenzfilter.png")
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt

filename = "Reflektion Interferenzfilter Spiegelseite.txt"
header_lines = 28  # 13

data = np.loadtxt(
    filename,
    skiprows=header_lines,
    delimiter="\t",
    converters={
        0: lambda s: float(s.replace(b",", b".")),
        1: lambda s: float(s.replace(b",", b".")),
    },
)

wavelength = data[:, 0]
intensity = data[:, 1]

plt.figure(figsize=(8, 5))

plt.plot(wavelength, intensity)

plt.xlabel("Wellenlänge (nm)")
plt.ylabel("Intensität <%>")
plt.title("Reflektion der Spiegelseite des grüne Interferenzfilters")

# Referenzlinie bei 543 nm
plt.axvline(x=542, linestyle="--", linewidth=1, color="red", label=f"CW = 542 nm")
# plt.axhline(y=47.10985, linestyle="--", linewidth=1, color="green", label="FWHM = 47.11 %")

plt.tight_layout()
plt.legend()
plt.savefig("Reflektion Spiegelseite.png")
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt

filename = "Reflektion Interferenzfilter Grünseite.txt"
header_lines = 34  # 13

data = np.loadtxt(
    filename,
    skiprows=header_lines,
    delimiter="\t",
    converters={
        0: lambda s: float(s.replace(b",", b".")),
        1: lambda s: float(s.replace(b",", b".")),
    },
)

wavelength = data[:, 0]
intensity = data[:, 1]

plt.figure(figsize=(8, 5))

plt.plot(wavelength, intensity)

plt.xlabel("Wellenlänge (nm)")
plt.ylabel("Intensität <%>")
plt.title("Reflektion der Farbseite des grünen Interferenzfilters")

# Referenzlinie bei 543 nm
plt.axvline(x=542, linestyle="--", linewidth=1, color="red", label=f"CW = 542 nm")
# plt.axhline(y=27.71141, linestyle="--", linewidth=1)

plt.tight_layout()
plt.legend()
plt.savefig("Reflektion Farbseite.png")
plt.show()
