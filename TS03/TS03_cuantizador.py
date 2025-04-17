#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TS03 - Cuantizador

El siguiente scipt implementa un cuantizador, pretende simular el error de 
cuantizacion y redondeo de un conversor A/D.




Created on Thu Apr 17 01:31:05 2025

@author: jchirino
"""

import numpy as np
import matplotlib.pyplot as plt

#Cuantizacion de Amplitud del vector de muestras,
# Recibe como datos 
#   xx:       Vector de muestras continuas en unidades fisicas [volt]
#   v_ref:    Tension de referencia del conversor A/D (supongo rango simetrico [-v_ref;v_ref])
#   n_bits:   Numero de bits del conversor A/D
# devuelve el vector de muestras cuantizado en palabras de n_bits
def func_cuantizador(xx, v_ref , n_bits):
    
    #manejo de errores, v_ref y n_bits validos
    if (n_bits <= 0):
        print("Parametro n_bits no valido, la cantidad de bits debe ser un entero positivo no nulo")
        return -1
    elif (v_ref == 0):
        print("Parametro v_ref no valido, la tension de referencia debe ser distita de 0")
        return -1
    else:
        #normalizo el vector de muestas
        xx = xx/v_ref
        #escalo el vector normalizado a el tamaño de palabra binaria 
        #del conversor A/D y redondeo al entero mas cercano
        xx_cuanttizado = np.round( np.pow(2, n_bits-1) * xx)
            
        return xx_cuanttizado



#Extraido de TS01 - Funcion para gegerar las muestras del Conversor A/D
def func_sen(A_max, DC_offset, Freq, Phase, N_sample, Fs):
    
    Ts = 1/Fs
    tt = np.arange(0,N_sample*Ts, Ts)
    xx = A_max * np.sin(2 * np.pi * Freq * tt + Phase) + DC_offset
    
    return xx

#Extraido de TS02 -Funcion para calcular la DFT apartir del vector de muestras xx
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


#%% INICIO DE EXPERIMENTO
#Parametos del Conversor A/D
#Conviene Normalizar la resolucion espectral a 1Hz haciendo N_sample=Fs 
N_sample= 100
Fs      = N_sample
Ts      = 1/Fs
v_ref   = 1 #Volt
n_bits  = 4


#Parametros de entrada del gegerador
A_max     = 1   #Amplitud [Volt]
DC_offset = 0   #Componente de continua [Volt]
F_0       = 4 #Frecuencia [Hz]
Phase     = 0   #fase [Rad]


# Defino el vector de tiempo
tt = np.arange(0, N_sample*Ts, Ts)

#Genero las muestras del Conversor A/D
xx = func_sen(A_max, DC_offset, F_0, Phase, N_sample, Fs)

#Cuantizo el amplitud el vector de muestras
xx_cuantizado = func_cuantizador(xx, v_ref, n_bits)


#Muestro el señal fisica
plt.figure(1)
plt.plot(tt, xx)
plt.title(f'Señal Senoidal,Fs={Fs}, F={ F_0}, fase= {Phase}')
plt.xlabel('Tiempo [Seg]')
plt.ylabel('Amplitud [Volt]')

#Muestro la señal cuantizada en amplitud
plt.figure(2)
plt.plot(tt, xx_cuantizado)
plt.title(f'Señal Senoidal cuantizada,v_ref={v_ref}, n_bits={n_bits}')
plt.xlabel('Tiempo [Seg]')
y_grid= np.arange(-np.pow(2,n_bits-1),np.pow(2,n_bits-1)+1,np.pow(2,n_bits-3)) #genero una grilla de multiplos de potencias de 2
plt.grid()
plt.ylabel('ADC Buffer [#]')

#%% Analisis del ruido de cuantizacion q 

#llevo el vector de muestras cuantizado de vuelta a unidade fisicas
xx_q_volt = v_ref * xx_cuantizado / np.pow(2,n_bits-1) 

#calculo el error de cuantizacion 
ee_q = xx_q_volt - xx

#Muestro el error de cuantizacion 
plt.figure(1)
plt.stem(tt, ee_q)  #error de cuantizacion
plt.plot(tt, np.ones(len(tt))*v_ref/np.pow(2,n_bits)) #cota superior +1/2 LSB
plt.plot(tt, np.ones(len(tt))*-v_ref/np.pow(2,n_bits)) #cota inferior -1/2 LSB
plt.title('Ruido de cuantizacion para secuencia de N_sample = {N_sample}')
plt.xlabel('Tiempo [Seg]')
plt.ylabel('Amplitud [Volt]')


#Calculo la DFT del error de cuantizacion
EE_q = func_DFT(ee_q)

EE_q_acorr = np.correlate(ee_q,ee_q)

#Calculo de la energia del ruido de cuantizacion mediante la varianza
LSB = 2*v_ref/np.pow(2,n_bits) # escalon de cuantizacion (less significant bit)
Energia_q = 1/12 * np.pow((LSB/2),2)

#Muestro la dft del error de cuantizacion
plt.figure(2)
plt.plot(np.arange(0,len(EE_q),1),np.abs(EE_q))
plt.title('DFT del ruido de cuantizacion')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()

#Muestro la autocorrelacion del error de cuantizacion
plt.figure(3)
plt.stem(np.arange(0,len(EE_q_acorr),1),np.abs(EE_q_acorr))
plt.plot(np.arange(0,len(EE_q_acorr),1),np.ones(len(tt))*v_ref/np.pow(2,n_bits-1))
plt.title('autocorrelacion del ruido de cuantizacion')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Energia')
plt.grid()

