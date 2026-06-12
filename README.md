# EDA de COVID-19 en Estados Unidos

Análisis exploratorio de los datos históricos recopilados por
[The COVID Tracking Project](https://covidtracking.com/data/download) hasta el
7 de marzo de 2021.

El proyecto estudia la evolución de casos, fallecimientos, pruebas y
hospitalizaciones, evalúa la calidad del dataset y compara el impacto entre
estados mediante valores absolutos y tasas por población.

## Entregables

- [Notebook completo del análisis](notebooks/01_eda_covid19.ipynb)
- [Informe ejecutivo en PDF](reports/informe_ejecutivo_covid19.pdf)
- [Dataset original](data/raw/all-states-history.csv)
- [Visualizaciones generadas](reports/figures)

## Principales hallazgos

- La ola más crítica se produjo durante el invierno de 2020-2021.
- Las hospitalizaciones alcanzaron su máximo el 6 de enero de 2021, con
  132.474 pacientes.
- La media móvil llegó a 247.111 casos diarios el 11 de enero de 2021.
- Los fallecimientos alcanzaron una media máxima de 3.335 diarios el
  13 de enero de 2021.
- La mayor correlación entre casos y fallecimientos aparece con un desfase
  aproximado de 16 días, con un coeficiente de Spearman de 0,798.
- California y Texas lideran los valores absolutos, pero el ranking cambia al
  ajustar por población.
- Dakota del Norte y Dakota del Sur presentan las tasas más altas de casos por
  100.000 habitantes.
- Nueva Jersey y Massachusetts encabezan la mortalidad por 100.000 habitantes.
- Se identificaron 141 registros con correcciones administrativas negativas.

## Contenido del EDA

El notebook incluye:

1. Carga reproducible del CSV mediante `requests`.
2. Comprensión inicial, tipos de datos y cobertura geográfica.
3. Análisis de valores ausentes y duplicados.
4. Selección y limpieza de variables.
5. Estadística descriptiva.
6. Análisis univariante y detección de valores atípicos.
7. Evolución diaria y mensual.
8. Análisis de pruebas y positividad aproximada.
9. Análisis bivariante y multivariante.
10. Matriz de correlación.
11. Estudio del desfase entre casos y fallecimientos.
12. Comparaciones territoriales absolutas y por 100.000 habitantes.
13. Conclusiones ejecutivas y limitaciones.

## Dataset

El archivo contiene:

- 20.780 registros.
- 41 variables.
- 56 jurisdicciones: los 50 estados, Washington D. C. y cinco territorios.
- Registros entre el 13 de enero de 2020 y el 7 de marzo de 2021.

Los datos demográficos utilizados para calcular tasas por 100.000 habitantes
proceden del
[Censo de Estados Unidos de 2020](https://www.census.gov/data/developers/data-sets/decennial-census.html).

## Estructura

```text
eda-covid19-usa/
├── data/
│   ├── raw/
│   │   └── all-states-history.csv
│   └── processed/
├── notebooks/
│   └── 01_eda_covid19.ipynb
├── reports/
│   ├── figures/
│   ├── build_final_report.py
│   └── informe_ejecutivo_covid19.pdf
├── requirements.txt
└── README.md
```

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/miguelRedondoWeb/eda-covid19-usa.git
cd eda-covid19-usa
```

Crear y activar un entorno virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Iniciar JupyterLab:

```bash
jupyter lab
```

Abrir `notebooks/01_eda_covid19.ipynb` y seleccionar:

```text
Kernel → Restart Kernel and Run All Cells
```

El notebook genera las visualizaciones dentro de `reports/figures` y el CSV
procesado dentro de `data/processed`.

Para reconstruir el informe ejecutivo:

```bash
python reports/build_final_report.py
```

## Tecnologías

- Python
- Requests
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Jupyter
- ReportLab

## Limitaciones

- El dataset termina el 7 de marzo de 2021.
- Los criterios y ritmos de notificación variaron entre jurisdicciones.
- La cobertura de hospitalización es incompleta, especialmente al inicio.
- Los datos de UCI y ventilación no permiten comparaciones generales fiables.
- La positividad calculada es una aproximación.
- Las correlaciones no demuestran causalidad.

## Autor

Miguel Redondo
