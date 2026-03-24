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
U = ufloat(13.11, 0.02)          #Spannung
I = ufloat(13.12, 0.02)          #Strom
P_zu = U * I            #zugeführte elektrische Leistung

U_cool = ufloat(7.26, 0.01)          #Spannung
I_cool  = ufloat(1.63, 0.01)          #Strom
P_cool = U_cool * I_cool           # ????
U_motor_cool = ufloat(231.5, 1)          #Spannung
I_motor_cool  = ufloat(0.38, 0.02)
P_motor_cool = U_motor_cool * I_motor_cool   

f_voll = ufloat(6.3, 0.05)           #Leerlauffrequenz
f_gebremst = ufloat(5.1, 0.05)       #Frequenz mit Bremszaum

r = ufloat(0.249, 0.001)          #Abstand der Kraftmessung zum Drehpunkt
F = ufloat(0.36, 0.01)          #Kraft
omega = 2 * np.pi * f_gebremst     #Winkelgeschwindigkeit
P_motor = r * F * omega     #Motorleistung 

T_1 = ufloat(200+273.15, 2)        #heiße Temperatur (upper bound 800°C)
T_2 = ufloat(10+273.15, 2)        #kalte Temperatur

data = [3.4970, 3.4120, 3.4150, 3.3960, 3.4280]          #Flächenintegrale der Kurve (Arbeit) Pa/m^3
dW_B = 0.0100           #Unsicherheit der Arbeit (Flächenintegral)
W = mean_with_uncertainty(data, dW_B)           #Arbeit (FLäche in Kurve, ACHTUNG Einheiten)




# %% 1. idealer Wirkungsgrad
n_ideal = (T_1 - T_2) / T_1
print(f"n_ideal ={n_ideal:.2f}")


# %% 1. unbelasteter Wirkungsgrad
n_unbel = (W * f_voll) / P_zu    
print(P_zu)                    #check das mit den fs nicht, kp was ma da braucchen, stimmt ws?
print(f"n_unbel ={n_unbel:.5f}")


# %% 1. belasteter Wirkungsgrad
n_bel = P_motor / P_zu
print(P_motor)
print(f"n_bel ={n_bel:.2f}")


# %% 1. mechanischer Wirkungsgrad
n_motor = P_motor / (W * f_gebremst)                    #check das mit den fs nicht, kp was ma da braucchen, stimmt ws?
print(f"n_motor ={n_motor:.2f}")


# %% 2.Wirkungsgrad Kältemaschine
n_cool = P_cool / P_motor
print(f"n_cool ={n_cool:.2f}")

