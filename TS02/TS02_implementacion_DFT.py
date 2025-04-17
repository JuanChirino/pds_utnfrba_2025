#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TPS02 -  Implementacion de la DFT 

El siguiente script Implementa la trasformada discreta de fourier apartir de 
un vector de muestras de entrada de longitud N. devolvera un vector de


    Xk=∑n=0N−1xn.e−j2π.k.n/N

    Como referencia ver ->https://www.youtube.com/watch?v=kjRkHIeb5eI


Created on Sat Apr 12 20:35:16 2025

@author: jchirino
"""

import numpy as np
import matplotlib.pyplot as plt


#Funcion para calcular la DFT apartir del vector de muestras xx
def func_DFT(xx): 

    N_sample = len(xx)
    nn = np.arange(0,N_sample,1)
   
    #genero la DFT apartir del producto interno entre el vector de muestas xx
    # y el vector de Twiddle factors ww_factors, tuve que calcular el primer
    # elemento a pata porque me tiraba un "NameError: name 'XX' is not defined"

    ww_factor = np.cos(2*np.pi*nn*0/N_sample) - 1j*np.sin(2*np.pi*nn*0/N_sample)
    XX = np.sum(xx*ww_factor)    
    
    
    for k in range(1,N_sample):
        #Genero el vector de Twiddle factors
        ww_factor = np.cos(2*np.pi*nn*k/N_sample) - 1j*np.sin(2*np.pi*nn*k/N_sample)
        XX = np.append( XX ,np.sum(xx*ww_factor))
    
    return XX



#Extraido de TS01 - Funcion para gegerar las muestras del Conversor A/D
def func_sen(A_max, DC_offset, Freq, Phase, N_sample, Fs):
    
    Ts = 1/Fs
    tt = np.arange(0,N_sample*Ts, Ts)
    xx = A_max * np.sin(2 * np.pi * Freq * tt + Phase) + DC_offset
    
    return xx
#%% 

##Ejemplo de uso

N_sample = 100
Fs = N_sample
F_0= 20 


#genero N_sample muestras de una senoidal
#Freq = F_0 Hz, 1V de amplitud, muestreada Fs=N_sample
xx = func_sen(1,0,F_0,0,N_sample,Fs)

XX = func_DFT(xx)

XX_angle = np.angle(XX) 
XX_module= np.abs(XX)

XX_fft = np.fft.fft(xx)

#Comparo los resultados
XX_error_abs = abs(XX) - abs(XX_fft)
XX_error_porc = (abs(XX) - abs(XX_fft)) / abs(XX_fft)

#Muestro las muestras de la señal
plt.figure(1)
plt.plot(np.arange(0,len(xx),1),xx)
plt.title(f'Secuencia Señal Senoidale: F0 = {F_0}; N_sample = {N_sample}')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [Volt]')
plt.grid()


#Muestro el resultado de la DFT
plt.figure(2)
plt.plot(np.arange(0,len(XX),1),abs(XX))
plt.title(f'DFT para secuencia de N_sample = {N_sample}')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()


plt.figure(3)
plt.plot(np.arange(0,len(XX),1),XX.real)
plt.plot(np.arange(0,len(XX),1),XX.imag)
plt.title(f'DFT para secuencia de N_sample = {N_sample}')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()




#%%
#Muestro el resultado de la FFT
plt.figure(3)
plt.plot(np.arange(0,len(XX_fft),1),abs(XX_fft))
plt.title(f'FFT para secuencia de N_sample = {N_sample}')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()


plt.figure(4)
plt.plot(np.arange(0,len(XX_fft),1),abs(XX_fft))
plt.title(f'FFT para secuencia de N_sample = {N_sample}')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()


#%%
#revisando la documentacion de Matplotlin.pyplot encontre esta funcion
# matplotlib.pyplot.magnitude_spectrum(x, *, Fs=None, Fc=None, window=None, pad_to=None, sides=None, scale=None, data=None, **kwargs)magnitude_spectrum
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.magnitude_spectrum.html#matplotlib.pyplot.magnitude_spectrum
#Muesta la mitad del espectro

plt.figure(3)
plt.magnitude_spectrum(xx,Fs)
plt.title('Magnitud del espectro usando pyploy.magnitude_spectrum')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()


#%%
#Muestro el error al calcularl a FT con distintos metodos
#error absoluto del modulo
plt.figure(4)
plt.plot(np.arange(0,len(XX_error_abs),1),abs(XX_error_abs))
plt.title('Error absoluto del modulo comparando DFT con FFT')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()

#error porcentual del modulo
plt.figure(5)
plt.plot(np.arange(0,len(XX_error_porc),1),abs(XX_error_porc))
plt.title('Error relativa del modulo comparando DFT con FFT')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('error/Valor_verdadero')
plt.grid()
