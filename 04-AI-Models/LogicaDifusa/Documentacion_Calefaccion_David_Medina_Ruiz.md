# Práctica 1.3: Sistema de Calefacción Automatizado con Lógica Difusa

**Autor:** David Medina Ruiz  
**Asignatura:** Modelos de IA  
**Fecha:** Diciembre 2025

---

## 1. Objetivo del Ejercicio

Programar un **sistema de calefacción automatizado** utilizando **lógica difusa**. El sistema debe:
- Leer datos de dos sensores: **temperatura** y **humedad**
- Determinar la **potencia de calefacción** adecuada basándose en reglas difusas
- Implementarse usando la biblioteca `skfuzzy` de Python

---

## 2. Especificaciones del Sistema

### 2.1. Variables de Entrada

#### **Temperatura**
- **Rango:** -10°C a 40°C
- **Conjuntos difusos:**
  - `baja`
  - `media`
  - `alta`
- **Espaciado:** Igualmente distribuidos en el rango

#### **Humedad**
- **Rango:** 0% a 100%
- **Conjuntos difusos:**
  - `baja`
  - `media`
  - `alta`
- **Espaciado:** Igualmente distribuidos en el rango

### 2.2. Variable de Salida

#### **Potencia**
- **Rango:** 0% a 100%
- **Conjuntos difusos:**
  - `muy baja`
  - `baja`
  - `media`
  - `alta`
  - `muy alta`

### 2.3. Reglas Difusas

El sistema implementa las siguientes reglas de inferencia:

| # | Condición | Consecuente |
|---|-----------|-------------|
| **Regla 1** | `temperatura alta` **Y** (`humedad alta` **O** `humedad media`) | `potencia muy baja` |
| **Regla 2** | `temperatura media` | `potencia baja` |
| **Regla 3** | `temperatura baja` | `potencia alta` |
| **Regla 4** | `temperatura baja` **Y** `humedad alta` | `potencia muy alta` |

**Interpretación de las reglas:**
- Cuando hace calor y hay humedad → Potencia mínima (no se necesita calentar)
- Cuando la temperatura es moderada → Potencia baja
- Cuando hace frío → Potencia alta
- Cuando hace mucho frío y hay mucha humedad → Potencia máxima (sensación térmica muy baja)

---

## 3. Implementación

### 3.1. Bibliotecas Utilizadas

```python
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
```

- **numpy:** Manejo de arrays y rangos numéricos
- **skfuzzy:** Implementación de lógica difusa
- **matplotlib:** Visualización de funciones de pertenencia

### 3.2. Definición de Variables Difusas

#### Antecedentes (Entradas)
```python
temperatura = ctrl.Antecedent(np.arange(-10, 41, 1), "temperatura")
humedad = ctrl.Antecedent(np.arange(0, 101, 1), "humedad")
```

#### Consecuente (Salida)
```python
potencia = ctrl.Consequent(np.arange(0, 101, 1), "potencia")
```

### 3.3. Funciones de Pertenencia

Se utilizó el método `automf()` para generar automáticamente funciones de pertenencia triangulares igualmente espaciadas:

```python
temperatura.automf(names=["baja", "media", "alta"])
humedad.automf(names=["baja", "media", "alta"])
potencia.automf(names=["muy baja", "baja", "media", "alta", "muy alta"])
```

### 3.4. Sistema de Reglas

```python
regla1 = ctrl.Rule(temperatura["alta"] & (humedad["alta"] | humedad["media"]), 
                   potencia["muy baja"])
regla2 = ctrl.Rule(temperatura["media"], potencia["baja"])
regla3 = ctrl.Rule(temperatura["baja"], potencia["alta"])
regla4 = ctrl.Rule(temperatura["baja"] & humedad["alta"], potencia["muy alta"])
```

### 3.5. Creación del Sistema de Control

```python
sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4])
simulador = ctrl.ControlSystemSimulation(sistema)
```

---

## 4. Pruebas y Resultados

### 4.1. Caso de Prueba 1: Condiciones Extremas de Frío

**Entradas:**
- Temperatura: -10°C
- Humedad: 100%

```python
simulador.inputs({"temperatura": -10, "humedad": 100})
simulador.compute()
```

**Resultado esperado:** Potencia muy alta (cercana al 100%)

**Regla activada:** Regla 4 (temperatura baja Y humedad alta → potencia muy alta)

**Interpretación:** En condiciones de frío extremo con alta humedad, el sistema activa la calefacción al máximo para compensar la sensación térmica muy baja.

### 4.2. Caso de Prueba 2: Condiciones Moderadas

**Entradas:**
- Temperatura: 25°C
- Humedad: 50%

```python
simulador.inputs({"temperatura": 25, "humedad": 50})
simulador.compute()
```

**Resultado esperado:** Potencia muy baja o baja

**Reglas activadas:** Regla 1 y Regla 2 (con diferentes grados de activación)

**Interpretación:** Con temperatura agradable, el sistema reduce la potencia de calefacción.

---

## 5. Visualización

El sistema incluye visualización gráfica de las funciones de pertenencia y el valor calculado:

```python
potencia.view(sim=simulador)
plt.show()
```

La gráfica muestra:
- **Eje X:** Valores de potencia (0-100%)
- **Eje Y:** Grado de pertenencia (0-1)
- **Curvas:** Las 5 categorías de potencia
- **Línea vertical:** El valor específico calculado por el sistema

---

## 6. Análisis de Resultados

### 6.1. Ventajas del Sistema Difuso

1. **Transiciones suaves:** No hay cambios bruscos en la potencia cuando las condiciones varían ligeramente
2. **Modelado del conocimiento experto:** Las reglas reflejan el razonamiento humano sobre cuándo calentar
3. **Manejo de incertidumbre:** El sistema puede trabajar con valores intermedios (ej: temperatura "algo baja")
4. **Múltiples reglas activas:** Varias reglas pueden contribuir simultáneamente al resultado final

### 6.2. Proceso de Inferencia

El sistema sigue estos pasos:

1. **Fuzzificación:** Convierte los valores numéricos de entrada en grados de pertenencia a conjuntos difusos
2. **Evaluación de reglas:** Calcula qué reglas se activan y en qué grado
3. **Agregación:** Combina las salidas de todas las reglas activas
4. **Defuzzificación:** Convierte el conjunto difuso resultante en un valor numérico de potencia

### 6.3. Comportamiento del Sistema

- **Frío extremo + Humedad alta:** Activa potencia máxima (Regla 4 domina)
- **Frío moderado:** Potencia alta (Regla 3)
- **Temperatura media:** Potencia baja (Regla 2)
- **Calor con humedad:** Potencia mínima (Regla 1)

---

## 7. Código Completo

```python
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definimos los rangos de valores que pueden tomar las variables difusas
temperatura = ctrl.Antecedent(np.arange(-10, 41, 1), "temperatura")
humedad = ctrl.Antecedent(np.arange(0, 101, 1), "humedad")
potencia = ctrl.Consequent(np.arange(0, 101, 1), "potencia")

# Definimos las funciones de pertenencia para cada variable difusa
temperatura.automf(names=["baja", "media", "alta"])
humedad.automf(names=["baja", "media", "alta"])
potencia.automf(names=["muy baja", "baja", "media", "alta", "muy alta"])

# Definimos las reglas y las asociamos con el sistema
regla1 = ctrl.Rule(temperatura["alta"] & (humedad["alta"] | humedad["media"]), 
                   potencia["muy baja"])
regla2 = ctrl.Rule(temperatura["media"], potencia["baja"])
regla3 = ctrl.Rule(temperatura["baja"], potencia["alta"])
regla4 = ctrl.Rule(temperatura["baja"] & humedad["alta"], potencia["muy alta"])

# Creamos el sistema de control
sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4])

# Creamos el simulador
simulador = ctrl.ControlSystemSimulation(sistema)

# Definimos entradas
simulador.inputs({"temperatura": -10, "humedad": 100})

# Realizamos la inferencia
simulador.compute()

# Imprimimos la salida
print("La potencia es:", simulador.output["potencia"])

# Visualización
potencia.view(sim=simulador)
plt.show()  # Mantiene la ventana de visualización abierta
```

---

## 8. Conclusiones

1. **Implementación exitosa:** El sistema cumple con todas las especificaciones del enunciado
2. **Lógica difusa efectiva:** Permite modelar el comportamiento de un sistema de calefacción de forma intuitiva
3. **Biblioteca skfuzzy:** Facilita la implementación de sistemas difusos en Python con sintaxis clara
4. **Aplicabilidad práctica:** Este tipo de sistemas se usa en termostatos inteligentes reales

### Posibles Mejoras

- Añadir más reglas para casos específicos
- Incluir más variables de entrada (hora del día, ocupación de la habitación)
- Ajustar las funciones de pertenencia basándose en datos reales
- Implementar funciones de pertenencia trapezoidales o gaussianas para mayor precisión

---

## 9. Referencias

- Documentación oficial de scikit-fuzzy: https://pythonhosted.org/scikit-fuzzy/
- Zadeh, L.A. (1965). "Fuzzy sets". Information and Control, 8(3), 338-353.
- Material de la asignatura Modelos de IA

---

**Fin del documento**
