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
def plot_function(
    file_path,
    x_label,
    y_label,
    title,
    plot_label,
    scale_y_log=False,
    inverting=False,
    converting=0,
    exception_cols=[],
    add_line_to_plot=0,
):
    "file_path: your file name (must be in same folder or provide relative path)\n"
    "x_label, y_label, title: self-explanatory\n"
    "plot_label: list of labels for the legend (must match number of pairs)\n"
    "scale_y_log: if True, y-axis will be logarithmic\n"
    "inverting: if True, y-values will be inverted (useful if u messed up the polarity)\n"
    "converting: if not 0 then x-values will be divided by this facotr (plug in your resistor value to convert from voltage to current as in ex.4.1)\n"
    "exception_cols: list of column indices to ignore (if u used add, you will have your input voltage twice, so you can ignore one of them here)\n"
    "add_line_to_plot: slope of the line to be added to the plot (default: 0, meaning no line) useful for 2.1 "

    def load_data(file_path):
        # Separator automatisch testen
        for sep in [";", ",", "\t"]:
            try:
                df = pd.read_csv(file_path, sep=sep)
                if df.shape[1] > 1:
                    print(f"Found the separator: '{sep}'")
                    return df
            except:
                pass

        raise ValueError("Could not read file. GGs.")

    def extract_xy_pairs(df):
        columns = df.columns
        data = df.values

        pairs = []
        if "time" in columns[0].lower() or "zeit" in columns[0].lower():
            for i in range(1, len(columns)):
                if i in exception_cols:
                    pass
                else:
                    x = data[:, 0]
                    y = data[:, i]

                    mask = ~np.isnan(x) & ~np.isnan(y)
                    x = x[mask]
                    y = y[mask]

                    if inverting:
                        y = -y

                    pairs.append((x, y, columns[0], columns[i]))

        else:
            for i in range(0, len(columns) - 1, 2):
                x = data[:, i]
                y = data[:, i + 1]

                # NaN entfernen
                mask = ~np.isnan(x) & ~np.isnan(y)
                x = x[mask]
                y = y[mask]

                if converting != 0:
                    x = x / converting
                pairs.append((x, y, columns[i], columns[i + 1]))

        return pairs

    if "LED" in title:
        # self explanatory, but you may have to adjust the colors if you had a different order of your LEDs
        colors = ["royalblue", "forestgreen", "gold", "firebrick"]
    else:
        colors = [
            "royalblue",
            "forestgreen",
            "firebrick",
            "darkorange",
            "purple",
            "darkblue",
            "pink",
            "gray",
        ]

    def plot_data(pairs):
        plt.figure()

        for i, (x, y, x_name, y_name) in enumerate(pairs):
            # x and y_name are currently not used, but you could use them to automatically generate the plot labels if you want
            label = f"{plot_label[i]}"
            plt.plot(x, y, linestyle="-", label=label, color=colors[i])

        if add_line_to_plot != 0:
            x_line = np.linspace(min(x), max(x), 100)
            y_line = add_line_to_plot * x_line
            plt.plot(
                x_line,
                y_line,
                color="firebrick",
                linestyle="-",
                label=f"y = {add_line_to_plot} * x",
            )
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        if scale_y_log:
            plt.yscale("log")

        plt.legend()
        plt.tight_layout()
        plt.show()

    df = load_data(file_path)

    # versuch Zahlen zu erzwingen (falls Komma/Strings drin sind)
    df = df.apply(pd.to_numeric, errors="coerce")

    pairs = extract_xy_pairs(df)

    print(f"Found datasets: {len(pairs)}")

    plot_data(pairs)


# %% Plotting von 2.1 Ohmscher Widerstand
plot_function(
    "2.1 Ohmscher Widerstand",
    x_label="Spannung (V)",
    y_label="Strom (mA)",
    title="Kennlinie eines Ohmschen Widerstands",
    plot_label=["Kennlinie eines 2 kΩ Widerstands"],
    scale_y_log=False,
    add_line_to_plot=0.5,
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
    + f"$n = {n_fit:.3f} \\pm {n_err:.3f}$"
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

# %% Merging tow CSV files
file_1 = "4.4 kalt"
file_2 = "4.4 warm"
merged_file = "4.4 kalt und warm.csv"

df1 = pd.read_csv(file_1, sep=",", decimal=".")
df2 = pd.read_csv(file_2, sep=",", decimal=".")
df2 = df2.iloc[:, 2:]
merged_df = pd.concat([df1, df2], axis=1)
merged_df.to_csv(merged_file, index=False)

# %% Plotting von 3.1 LED Brückengleichrichter
plot_function(
    "3.1 LED Brückengleichrichter",
    x_label="Zeit (s)",
    y_label="Spannung (V)",
    title="Brückengleichrichter mit LEDs",
    plot_label=["Eingangsspannung", "Last-Ausgangsspannung"],
    scale_y_log=False,
    inverting=True,
)

# %% Plotting von 3.3 Dioden Brückengleichrichter und Berechnung der Brummspannung
plot_function(
    "3.3 Brückengleichrichter mit-ohne Glättungskondi",
    x_label="Zeit (s)",
    y_label="Spannung (V)",
    title="Brückengleichrichter mit Dioden (mit und ohne Glättungskondensator)",
    plot_label=[
        "Eingangsspannung",
        "Last-Ausgangsspannung (C = 0 µF)",
        "Last-Ausgangsspannung (C = 10 µF)",
        "Last-Ausgangsspannung (C = 1 µF)",
    ]
    * 4,
    exception_cols=[3, 5],
    inverting=True,
)
df = pd.read_csv(
    "3.3 Brückengleichrichter mit-ohne Glättungskondi", sep=",", decimal="."
)
print(f"Brummspannung 1 µF: {max(abs(df.iloc[:, 6])) - min(abs(df.iloc[:, 6]))} V")
print(f"Brummspannung 10 µF: {max(abs(df.iloc[:, 4])) - min(abs(df.iloc[:, 4]))} V")

# %% 4.1 Plotting von Stromsteuerkennlinie
# --- Daten einlesen ---
file_path = "4.1 Stromsteuerkennlinie (noch umzurechnern in I_B)"

resistor_value = 100  # in kOhm, für die Umrechnung von U_BE zu I_B von V zu mA

data = pd.read_csv(file_path, sep=",", decimal=".")

# Spalten anpassen!
U_BE = data.iloc[:, 0].values  # Basisspannung
I_C = data.iloc[:, 1].values  # Kollektorstrom

I_B = U_BE / resistor_value  # Umrechnung in Basisstrom

# --- Linearen Bereich wählen ---
mask = (I_B > 0.1 / resistor_value) & (I_B < 0.3 / resistor_value)

I_B_fit = I_B[mask]
I_C_fit = I_C[mask]

# --- Linearer Fit ---
result = linregress(I_B_fit, I_C_fit)
slope = result.slope
intercept = result.intercept
std_err = result.stderr
intercept_stdr = result.intercept_stderr

beta = slope

print(f"Beta (Verstärkung) = {beta:.2f} ± {std_err:.2f}")
print(f"Intercept = {intercept:.3e} ± {intercept_stdr:.3e}")
print(f"R^2 = {result.rvalue**2:.4f}")

# --- Plot ---
plt.figure()
plt.plot(I_B, I_C, linestyle="-", label="Stromsteuerkennlinie")
axis_values = np.linspace(0.0 / resistor_value, 0.35 / resistor_value, 100)
plt.plot(
    axis_values,
    slope * axis_values + intercept,
    color="red",
    label="linearer Fit: y = A * x + B",
)
plt.axvspan(0.1 / resistor_value, 0.3 / resistor_value, alpha=0.2, label="Fitbereich")
plt.xlabel("Basisstrom I_B (mA)")
plt.ylabel("Kollektorstrom I_C (mA)")
plt.title("Stromsteuerkennlinie in Emitterschaltung mit linearem Fit")
plt.legend()
plt.grid()

plt.show()

# %% 4.2 Plotting von Ausgangskennlinienfeld
plot_function(
    "4.2 Ausgangskennlinienfeld",
    x_label="Spannung U_CE (V)",
    y_label="Strom I_C (mA)",
    title="Ausganskennlinienfeld mit variablen U_BE",
    plot_label=["U_BE = 0.6 V", "U_BE = 0.633 V", "U_BE = 0.666 V", "U_BE = 0.7 V"],
    scale_y_log=False,
)


# %% 4.3 Kleinsignalverstärkung ohne Stromgegenkopplung
plot_function(
    "4.3 kalt und warm.csv",
    x_label="Zeit (µs)",
    y_label="Spannung (V)",
    title="Kleinsignalverstärkung in Emitterschaltung ohne Stromgegenkopplung",
    plot_label=[
        "u_e",
        "u_a bei Raumtemperatur",
        "u_a nach Erhitzung",
    ],
)
df = pd.read_csv("4.3 kalt und warm.csv", sep=",", decimal=".")
print(
    f"Kleinsignalverstärkung Raumtemperatur: {max(df.iloc[:, 2]) / max(df.iloc[:, 1])} "
)
print(f"Kleinsignalverstärkung Erhitzung: {max(df.iloc[:, 3]) / max(df.iloc[:, 1])} ")

# %% 4.4 Kleinsignalverstärkung mit Stromgegenkopplung
plot_function(
    "4.4 kalt und warm.csv",
    x_label="Zeit (µs)",
    y_label="Spannung (V)",
    title="Kleinsignalverstärkung in Emitterschaltung mit Stromgegenkopplung",
    plot_label=[
        "u_e",
        "u_a bei Raumtemperatur",
        "u_a nach Erhitzung",
    ],
)
df = pd.read_csv("4.4 kalt und warm.csv", sep=",", decimal=".")
print(
    f"Kleinsignalverstärkung Raumtemperatur: {max(df.iloc[:, 2]) / max(df.iloc[:, 1])} "
)
print(f"Kleinsignalverstärkung Erhitzung: {max(df.iloc[:, 3]) / max(df.iloc[:, 1])} ")

# %%
