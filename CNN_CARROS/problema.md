# Problema: Clasificación de Clientes según su Perfil Financiero

## Descripción del Problema

Una institución financiera desea clasificar a sus clientes en tres categorías basándose en su perfil financiero y de comportamiento:

- Riesgo Bajo: Clientes que cumplen con todos los pagos a tiempo y tienen ingresos estables.
- Riesgo Medio: Clientes con retrasos esporádicos en los pagos o ingresos variables.
- Riesgo Alto: Clientes con historial de impagos o ingresos inestables.

## Características de Entrada:

Historial de pagos: Porcentaje de pagos realizados a tiempo (normalizado entre 0 y 1).
Ingresos mensuales: Ingresos promedio del cliente (normalizado entre 0 y 1).
Relación deuda-ingreso: Proporción entre la deuda total y los ingresos totales (normalizado entre 0 y 1).
Categorías de Salida:

`Riesgo Bajo`: [1, 0, 0]
`Riesgo Medio`: [0, 1, 0]
`Riesgo Alto`: [0, 0, 1]

## Conjunto de Datos de Entrenamiento

Historial de pagos	Ingresos mensuales	Relación deuda-ingreso	Resultado
0.9	0.8	0.2	[1, 0, 0]
0.7	0.6	0.5	[0, 1, 0]
0.4	0.4	0.8	[0, 0, 1]
0.8	0.9	0.3	[1, 0, 0]
0.5	0.7	0.6	[0, 1, 0]
0.3	0.5	0.9	[0, 0, 1]

## Actividades

Implementar una red neuronal multicapa para clasificar los clientes según su riesgo.
Encontrar los valores óptimos para los pesos `w1`, `w2` 'wn' y el sesgo `b` mediante entrenamiento.
Graficar la frontera de decisión que separa los clientes .
¿Son los datos linealmente separables?
¿Qué ajustes podrían hacer al modelo para mejorar la clasificación?
Describir cada una de las partes del modelo implementando