# %% global imports and functions
import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat

def mean_with_uncertainty(values, u_B=0):
    values = np.array(values)
    N = len(values)

    mean = np.mean(values)
    if N > 1:
        s = np.std(values, ddof=1)          # Stichproben-Stdabw
        u_A = s / np.sqrt(N)
    else:
        u_A = 0

    u_total = np.sqrt(u_A**2 + u_B**2)
    
    return ufloat(mean, u_total)



# %% 1.Generell
U = ufloat(,)          #Spannung
I = ufloat(,)          #Strom
P_zu = U * I            #zugeführte elektrische Leistung

U_cool = ufloat(,)          #Spannung
I_cool  = ufloat(,)          #Strom
P_cool = U_cool * I_cool           # ????

f_voll = ufloat(,)           #Leerlauffrequenz
f_gebremst = ufloat(,)       #Frequenz mit Bremszaum

r = ufloat(,)          #Abstand der Kraftmessung zum Drehpunkt
F = ufloat(,)          #Kraft
omega = 2 * np.pi * f_gebremst     #Winkelgeschwindigkeit
P_motor = r * F * omega     #Motorleistung 

T_1 = ufloat(+273.15,)        #heiße Temperatur
T_2 = ufloat(+273.15,)        #kalte Temperatur

data = [,,,]          #Flächenintegrale der Kurve (Arbeit)
dW_B =           #Unsicherheit der Arbeit (Flächenintegral)
W = mean_with_uncertainty(data, dW_B)           #Arbeit (FLäche in Kurve, ACHTUNG Einheiten)




# %% 1. idealer Wirkungsgrad
n_ideal = (T_1 - T_2) / T_1
print(f"n_ideal ={n_ideal:.2f}")


# %% 1. unbelasteter Wirkungsgrad
n_unbel = (W * f_voll) / P_zu                        #check das mit den fs nicht, kp was ma da braucchen, stimmt ws?
print(f"n_unbel ={n_unbel:.2f}")


# %% 1. belasteter Wirkungsgrad
n_bel = P_motor / P_zu
print(f"n_bel ={n_bel:.2f}")


# %% 1. mechanischer Wirkungsgrad
n_motor = P_motor / (W * f_voll)                    #check das mit den fs nicht, kp was ma da braucchen, stimmt ws?
print(f"n_motor ={n_motor:.2f}")


# %% 2.Wirkungsgrad Kältemaschine
n_cool = P_cool / P_motor
print(f"n_cool ={n_cool:.2f}")