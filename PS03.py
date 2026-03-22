# %% global imports
import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat

# %% 1.Generell
U = ufloat(,)          #Spannung
I = ufloat(,)          #Strom
U_cool = ufloat(,)          #Spannung
I_cool  = ufloat(,)          #Strom
r = ufloat(,)          #Abstand der Kraftmessung zum Drehpunkt
F = ufloat(,)          #Kraft
T_1 = ufloat(+273.15,)        #heiße Temperatur
T_2 = ufloat(+273.15,)        #kalte Temperatur
W = ufloat(,)           #Arbeit (FLäche in Kurve, ACHTUNG Einheiten)
f = ufloat(,)           #Leerlauffrequenz
P_zu = U * I            #zugeführte elektrische Leistung
P_cool = U_cool * I_cool           # ????
omega = 2 * np.pi * f     #Winkelgeschwindigkeit
P_motor = r * F * omega     #Motorleistung 


# %% 1. idealer Wirkungsgrad
n_ideal = (T_1 - T_2) / T_1
print(f"n_ideal ={n_ideal:.2f}")


# %% 1. unbelasteter Wirkungsgrad
n_unbel = (W * f) / P_zu
print(f"n_unbel ={n_unbel:.2f}")


# %% 1. belasteter Wirkungsgrad
n_bel = P_motor / P_zu
print(f"n_bel ={n_bel:.2f}")


# %% 1. mechanischer Wirkungsgrad
n_motor = P_motor / (W * f)
print(f"n_motor ={n_motor:.2f}")


# %% 2.Wirkungsgrad Kältemaschine
n_cool = P_cool / P_motor
print(f"n_cool ={n_cool:.2f}")