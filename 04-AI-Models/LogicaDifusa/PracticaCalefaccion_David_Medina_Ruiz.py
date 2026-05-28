import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

#Definimos los rangos de valores que pueden tomar las variables difusas
temperatura = ctrl.Antecedent(np.arange(-10,41,1),"temperatura")
humedad = ctrl.Antecedent(np.arange(0,101,1),"humedad")
potencia = ctrl.Consequent(np.arange(0,101,1),"potencia")

#Definimos las funciones de pertenencia para cada variable difusa
temperatura.automf(names=["baja","media","alta"])
humedad.automf(names=["baja","media","alta"])
potencia.automf(names=["muy baja","baja","media","alta","muy alta"])

#Definimos las reglas y las asociamos con el sistema
regla1 = ctrl.Rule(temperatura["alta"] & (humedad["alta"] | humedad["media"]), potencia["muy baja"])
regla2 = ctrl.Rule(temperatura["media"], potencia["baja"])
regla3 = ctrl.Rule(temperatura["baja"], potencia["alta"])
regla4 = ctrl.Rule(temperatura["baja"] & humedad["alta"], potencia["muy alta"])

#Creamos el sistema de control
sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4])

#Creamos el simulador
simulador = ctrl.ControlSystemSimulation(sistema)

#Definimos entradas
simulador.inputs({"temperatura":35, "humedad":80})

#Realizamos la inferencia
simulador.compute()

#Imprimimos la salida
print("La potencia es:", simulador.output["potencia"])
potencia.view(sim=simulador) # Muestra la gráfica de la salida
plt.show()  # Mantiene la ventana de visualización abierta
