# Analisis exploratorio de COVID-19 en Estados Unidos

## Objetivo

Transformar los datos historicos de The COVID Tracking Project en informacion
clara para una audiencia ejecutiva.

La pregunta principal del analisis sera:

> Como evoluciono la presion de la pandemia en Estados Unidos y que estados
> concentraron los peores resultados hasta el 7 de marzo de 2021?

## Preguntas de negocio

1. Como evolucionaron los casos, fallecimientos y hospitalizaciones?
2. Cuales fueron los principales picos de la pandemia?
3. Que estados registraron mas casos y fallecimientos?
4. Que relacion existe entre casos, hospitalizaciones y fallecimientos?
5. Que limitaciones de calidad presentan los datos?

## Estructura

```text
EDA/
|-- data/
|   |-- raw/          # Datos originales, sin modificar
|   `-- processed/    # Datos limpios
|-- notebooks/        # Analisis paso a paso
|-- reports/
|   `-- figures/      # Graficos finales
|-- src/              # Funciones reutilizables
|-- README.md
`-- requirements.txt
```

## Plan de trabajo

1. Carga y comprension del dataset.
2. Evaluacion de calidad: tipos, nulos, duplicados e inconsistencias.
3. Limpieza y seleccion de variables.
4. Analisis univariante y temporal.
5. Comparacion entre estados.
6. Creacion de visualizaciones ejecutivas.
7. Redaccion de conclusiones, limitaciones y recomendaciones.

## Dataset

- Fuente: The COVID Tracking Project.
- Archivo: `data/raw/all-states-history.csv`.
- Cobertura: datos diarios de estados y territorios de EE. UU.
- Fecha final: 7 de marzo de 2021.
- Nota: el proyecto dejo de recopilar datos despues de esa fecha.

## Variables iniciales de interes

- `date`: fecha del registro.
- `state`: abreviatura del estado o territorio.
- `positive`: casos acumulados.
- `positiveIncrease`: nuevos casos diarios.
- `death`: fallecimientos acumulados.
- `deathIncrease`: nuevos fallecimientos diarios.
- `hospitalizedCurrently`: pacientes hospitalizados en ese momento.
- `inIcuCurrently`: pacientes en UCI en ese momento.
- `onVentilatorCurrently`: pacientes con ventilacion en ese momento.
- `totalTestResults`: resultados de pruebas acumulados.

## Entregables

- Notebook reproducible con el EDA.
- Dataset limpio.
- Graficos guardados en `reports/figures`.
- Informe ejecutivo con la historia encontrada en los datos.

