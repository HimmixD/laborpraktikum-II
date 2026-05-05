# %%
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import linregress

sys.path.append(os.path.dirname(__file__))


# %% definieren einer Funktion zum Einlesen und Plotten von Daten aus CSV-Dateien
def plot_function(file_path, x_label, y_label, title, plot_label, scale_y_log=False):
    # separator = None  # None = auto-detect
    # decimal = None  # None = auto-detect

    # =========================
    # AUTO LOAD FUNCTION
    # =========================
    def load_data(file_path):
        # Separator automatisch testen
        for sep in [";", ",", "\t"]:
            try:
                df = pd.read_csv(file_path, sep=sep)
                if df.shape[1] > 1:
                    print(f"[INFO] Separator erkannt: '{sep}'")
                    return df
            except:
                pass

        raise ValueError("Konnte Datei nicht lesen. Willkommen im Chaos.")

    # =========================
    # DATA PARSING
    # =========================
    def extract_xy_pairs(df):
        columns = df.columns
        data = df.values

        pairs = []
        if len(columns) % 2 != 0:
            for i in range(1, len(columns)):
                x = data[:, 0]
                y = data[:, i]

                mask = ~np.isnan(x) & ~np.isnan(y)
                x = x[mask]
                y = y[mask]

                pairs.append((x, y, columns[0], columns[i]))

        else:
            # gehe spaltenweise durch (0/1, 2/3, ...)
            for i in range(0, len(columns) - 1, 2):
                x = data[:, i]
                y = data[:, i + 1]

                # NaN entfernen
                mask = ~np.isnan(x) & ~np.isnan(y)
                x = x[mask]
                y = y[mask]

                pairs.append((x, y, columns[i], columns[i + 1]))

        return pairs

    # =========================
    # PLOTTING
    # =========================
    colors = [
        "royalblue",
        "forestgreen",
        "gold",
        "firebrick",
        "purple",
        "brown",
        "pink",
        "gray",
    ]

    def plot_data(pairs):
        plt.figure()

        for i, (x, y, x_name, y_name) in enumerate(pairs):
            label = f"{plot_label[i]}"
            plt.plot(x, y, linestyle="-", label=label, color=colors[i])

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        if scale_y_log:
            plt.yscale("log")

        plt.legend()
        plt.tight_layout()
        plt.show()

    # =========================
    # MAIN
    # =========================
    df = load_data(file_path)

    # versuch Zahlen zu erzwingen (falls Komma/Strings drin sind)
    df = df.apply(pd.to_numeric, errors="coerce")

    pairs = extract_xy_pairs(df)

    print(f"[INFO] Gefundene Datensätze: {len(pairs)}")

    plot_data(pairs)


# %% Plotting von 2.1 Ohmscher Widerstand
plot_function(
    "2.1 Ohmscher Widerstand",
    x_label="Spannung (V)",
    y_label="Strom (mA)",
    title="Kennlinie eines Ohmschen Widerstands",
    plot_label=["Kennlinie"],
    scale_y_log=False,
)
# %% Fitting von 2.2 Si Diode
# =========================
# USER SETTINGS
# =========================

file_path = "2.2 Si Diode"  # Pfad zur CSV-Datei mit den Diodendaten

# Fitbereich (in Volt)
U_min = 0
U_max = 0.69

title = "Kennlinie einer Si-Diode mit Shockley-Fit"

# Konstanten
k = 1.380649e-23
q = 1.602176634e-19
T = 300
U_T = k * T / q

# =========================
# MODEL
# =========================


def shockley(U, I_s, n):
    return I_s * (np.exp(U / (n * U_T)) - 1)


# =========================
# DATA LOAD
# =========================

data = pd.read_csv(file_path, sep=",", decimal=".")

U = pd.to_numeric(data.iloc[:, 0], errors="coerce").values
I = pd.to_numeric(data.iloc[:, 1], errors="coerce").values

# NaN entfernen
mask = ~np.isnan(U) & ~np.isnan(I)
U = U[mask]
I = I[mask]

# =========================
# FIT-BEREICH AUSWÄHLEN
# =========================

fit_mask = (U >= U_min) & (U <= U_max)

U_fit = U[fit_mask]
I_fit = I[fit_mask]

# =========================
# FIT
# =========================

initial_guess = [1e-12, 1.5]

params, covariance = curve_fit(shockley, U_fit, I_fit, p0=initial_guess)

I_s_fit, n_fit = params

# Unsicherheiten (Standardabweichungen)
errors = np.sqrt(np.diag(covariance))
I_s_err, n_err = errors

print("==== FIT ERGEBNISSE ====")
print(f"I_s = ({I_s_fit:.3e} ± {I_s_err:.3e}) mA")
print(f"n   = ({n_fit:.3f} ± {n_err:.3f})")

# =========================
# PLOT
# =========================

plt.figure()

# komplette Daten
plt.scatter(U, I, s=10, label="Messdaten")

# Fitkurve über gesamten Bereich
U_plot = np.linspace(min(U), max(U), 500)
I_plot = shockley(U_plot, I_s_fit, n_fit)
plt.plot(U_plot, I_plot, color="red", label="Fit (Shockley)")

# Log-Skala (wichtig!)
# plt.yscale("log")

plt.xlabel("Spannung (V)")
plt.ylabel("Strom (mA)")
plt.title(title)
plt.grid()
plt.legend()

# =========================
# TEXTBOX MIT FIT
# =========================

fit_text = (
    r"$I = I_s (e^{U/(n U_T)} - 1)$"
    "\n"
    + f"$I_s = ({I_s_fit:.2e} \\pm {I_s_err:.2e})$ mA\n"
    + f"$n = {n_fit:.2f} \\pm {n_err:.2f}$"
)

plt.text(
    0.05,
    0.1,
    fit_text,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="bottom",
    bbox=dict(boxstyle="round", alpha=0.8),
)

plt.tight_layout()
plt.show()

# %% Plotting von 2.3 Zenerdioden
plot_function(
    "2.3 Zenerdioden",
    x_label="Spannung (V)",
    y_label="Strom (mA)",
    title="Kennlinien von Zener-Dioden",
    plot_label=[
        "Kennlinie der 2.4 V Zenerdiode",
        "Kennlinie der 3.0 V Zenerdiode",
        "Kennlinie der 3.6 V Zenerdiode",
        "Kennlinie der 4.3 V Zenerdiode",
    ],
    scale_y_log=False,
)
# %% Plotting von 2.4 LEDs
plot_function(
    "2.4 LEDs",
    x_label="Spannung (V)",
    y_label="Strom (mA)",
    title="Kennlinien von LEDs",
    plot_label=[
        "Kennlinie der blauen LED",
        "Kennlinie der grünen LED",
        "Kennlinie der gelben LED",
        "Kennlinie der roten LED",
    ],
    scale_y_log=False,
)
# %% Splitten von 2.5 Spektrallinien LEDs in einzelne CSV-Dateien
# =========================
# SETTINGS
# =========================

file_path = "Spektrallinien LEDs.csv"
output_prefix = "output_pair"

# =========================
# HELPER: STRING → FLOAT
# =========================


def to_float_safe(series):
    # alles in string
    s = series.astype(str)

    # komma → punkt (deutsches format)
    s = s.str.replace(",", ".", regex=False)

    # alles entfernen was keine zahl ist (inkl. einheiten)
    s = s.str.replace(r"[^0-9eE\.\-\+]", "", regex=True)

    return pd.to_numeric(s, errors="coerce")


# =========================
# LOAD DATA
# =========================


def load_data(file_path):
    for sep in [";", ",", "\t"]:
        try:
            df = pd.read_csv(file_path, sep=sep)
            if df.shape[1] > 1:
                print(f"[INFO] Separator erkannt: '{sep}'")
                return df
        except:
            pass

    raise ValueError("Datei unlesbar. Glückwunsch.")


df = load_data(file_path)

columns = df.columns

pair_count = 0

# =========================
# SPLIT
# =========================

for i in range(0, len(columns) - 1, 2):
    x_raw = df.iloc[:, i]
    y_raw = df.iloc[:, i + 1]

    # KONVERTIEREN (jetzt robust)
    x = to_float_safe(x_raw)
    y = to_float_safe(y_raw)

    # gültige werte behalten
    mask = ~np.isnan(x) & ~np.isnan(y)

    x_clean = x[mask]
    y_clean = y[mask]

    if len(x_clean) == 0:
        print(f"[WARNUNG] Paar {i//2+1} hat keine gültigen Daten → übersprungen")
        continue

    new_df = pd.DataFrame({columns[i]: x_clean, columns[i + 1]: y_clean})

    output_file = f"{output_prefix}_{pair_count+1}.csv"
    new_df.to_csv(output_file, index=False)

    print(f"[INFO] Gespeichert: {output_file} ({len(new_df)} Punkte)")

    pair_count += 1

print(f"[INFO] Fertig. {pair_count} Dateien erstellt.")

# %% Plotting von 3.1 LED Brückengleichrichter
plot_function(
    "3.1 LED Brückengleichrichter",
    x_label="Zeit (s)",
    y_label="Spannung (V)",
    title="Brückengleichrichter mit LEDs",
    plot_label=["Eingangsspannung", "Last-Ausgangsspannung"],
    scale_y_log=False,
)

# %% Plotting von 3.3 Dioden Brückengleichrichter
plot_function(
    "3.3 Brückengleichrichter mit-ohne Glättungskondi",
    x_label="Zeit (s)",
    y_label="Spannung (V)",
    title="Brückengleichrichter mit Dioden (mit und ohne Glättungskondensator)",
    plot_label=["Eingangsspannung", "Last-Ausgangsspannung"] * 2,
    scale_y_log=False,
)
"need to delete the duplicates in my pairs (Eingagnsspannung wird öfter geplottet)"


# %%
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
