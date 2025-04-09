#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TPS01 -  Generador de Señal Senoidal 

El siguiente script pretende emular un generador de funciones de laboratorio
recibe como parametros de entrada

    la amplitud máxima de la senoidal (volts)
    su valor medio (volts)
    la frecuencia (Hz)
    la fase (radianes)
    la cantidad de muestras digitalizada por el ADC (# muestras)
    la frecuencia de muestreo del ADC.

    
Devuelve un vector de tiempos y amplitudes con la funcion generada

tt, xx 


Created on Sun Mar 30 03:12:15 2025

@author: jchirino
"""
import numpy as np
import matplotlib.pyplot as plt


#Parametros de entrada del gegerador

A_max = 0.5     #Amplitud [Volt]
DC_offset = 0.5 #Componente de continua [Volt]
Freq = 10.0     #Frecuencia [Hz]
Phase = 0.0     #fase [Rad]

#Parametos del Conversor A/D
#Conviene Normalizar la resolucion espectral a 1Hz haciendo N_sample=Fs 
N_sample = 1000
Fs = 1000
Ts = 1/Fs



# Defino el vector de tiempo, se prefiere usar arrage() en lugar de linspace()
# Ya que se tiene certeza sobre la cantidad de elementos que incluye el vector
tt = np.arange(0, N_sample*Ts, Ts)


#Genero las muestras del Conversor A/D
xx = A_max * np.sin(2 * np.pi * Freq * tt + Phase) + DC_offset


#Muestro el resultado
plt.plot(tt, xx)
plt.title('Generador de Señal Senoidal')
plt.xlabel('Tiempo [Seg]')
plt.ylabel('Amplitud [Volt]')


