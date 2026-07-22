# Reto Macroentorno — Pipeline de Datos, RPA y Dashboard en Power BI

## 1. Descripción del proyecto

Este proyecto implementa un pipeline de datos para integrar, transformar y analizar información pública del macroentorno ecuatoriano. La solución combina fuentes del Banco Central del Ecuador, INEC, Superintendencia de Compañías y MINEDUC, siguiendo una arquitectura por capas RAW, Silver y Gold.

El sistema procesa archivos recibidos desde un flujo de RPA, transforma los datos, genera tablas y archivos Gold, y actualiza un dashboard de Power BI con tres páginas analíticas.

El proyecto fue desarrollado en Python 3.13 y utiliza SQLite como base de datos principal.

---

## 2. Objetivo

Construir un sistema integrado capaz de:

- Recibir archivos descargados por el equipo de RPA.
- Procesar automáticamente archivos de distintas fuentes.
- Almacenar la información en una base de datos SQLite.
- Generar tablas Gold orientadas al análisis.
- Exportar resultados a CSV.
- Actualizar un dashboard de Power BI.
- Responder tres preguntas analíticas relacionadas con economía, empleo, actividad empresarial y demanda educativa.

---

## 3. Preguntas analíticas del dashboard

### P1. ¿Cómo ha evolucionado la economía ecuatoriana en los últimos 20 años?

La primera página analiza:

- Evolución del PIB per cápita nominal.
- Variación anual del PIB.
- Clasificación del ciclo económico.
- Último valor del PIB per cápita.
- Variación interanual más reciente.
- Índice de Expectativas Empresariales del último año.

### P2. ¿En qué sectores y provincias se concentran la actividad económica y el empleo?

La segunda página analiza:

- Concentración del VAB por provincia.
- Principales indicadores nacionales de empleo.
- Sectores CIIU con mayor aporte económico.
- Tasa de desempleo más reciente.

### P3. ¿Dónde se concentra la población estudiantil y cuántas empresas activas existen por provincia?

La tercera página compara:

- Estudiantes de educación ordinaria por provincia.
- Empresas activas por provincia.
- Ratio de estudiantes por empresa.
- Provincias con mayor concentración estudiantil en relación con la actividad empresarial.

> Nota metodológica: la fuente oficial de MINEDUC utilizada está agregada por institución educativa y no contiene desagregación por grado o curso. Por esta razón, se utiliza el total de estudiantes de educación ordinaria como aproximación territorial de la demanda educativa y no como conteo exclusivo de estudiantes de tercero de Bachillerato.

---

## 4. Arquitectura del pipeline

La solución sigue una arquitectura de tres capas:

### RAW

Contiene los archivos y registros originales recibidos desde las fuentes y desde el flujo RPA.

Ejemplos:

- Archivos SQL de SUPERCIAS.
- Archivos CSV y Excel del BCE.
- Archivos del INEC.
- Archivos de MINEDUC.
- Registros almacenados en `raw_supercias_consolidado`.

### Silver

Contiene datos limpios, estructurados y normalizados.

Ejemplos:

- `fact_empresas_rpa`
- `fact_ranking_empresas_rpa`
- tablas de indicadores macroeconómicos
- tablas de empleo
- tablas geográficas y temporales

### Gold

Contiene datos preparados para análisis y visualización.

Principales tablas y archivos:

- `gold_empresas_provincia`
- `gold_empresas_situacion`
- `gold_empresas_ciiu`
- `gold_ranking_provincia_anio`
- `gold_ranking_ciiu_anio`
- `gold_resumen_supercias`
- `gold_bachilleres_vs_empresas`

---

## 5. Fuentes de datos

### Banco Central del Ecuador

- PIB real.
- PIB per cápita nominal.
- VAB por provincia y sector.
- Precio del petróleo WTI.
- Riesgo país.
- Índice de Expectativas Empresariales.

### INEC

- ENEMDU.
- Indicadores laborales.
- Información de ocupación y ramas de actividad.

### Superintendencia de Compañías

- Directorio de compañías.
- Ranking empresarial.
- Situación legal.
- Provincia.
- Cantón.
- CIIU.
- Información financiera.

### MINEDUC

Archivo utilizado:

`data_raw/mineduc/amie_2009_2024_inicio.csv`

Campos principales:

- Año lectivo.
- Provincia.
- Cantón.
- Institución.
- Tipo de educación.
- Sostenimiento.
- Total de estudiantes.

---

## 6. Estructura del proyecto

```text
reto_macroentorno/
│
├── data_raw/
│   ├── bce/
│   ├── inec/
│   ├── mineduc/
│   └── supercias/
│
├── db/
│   └── macroentorno.db
│
├── gold/
│   ├── supercias/
│   │   ├── gold_empresas_provincia.csv
│   │   ├── gold_empresas_situacion.csv
│   │   ├── gold_empresas_ciiu.csv
│   │   ├── gold_ranking_provincia_anio.csv
│   │   ├── gold_ranking_ciiu_anio.csv
│   │   └── gold_resumen_supercias.csv
│   │
│   └── gold_bachilleres_vs_empresas.csv
│
├── powerbi_csv/
│   └── fact_mineduc_bachilleres.csv
│
├── transform/
│   ├── rpa_parser.py
│   ├── transformar_supercias_json.py
│   ├── crear_gold_supercias.py
│   ├── exportar_gold_supercias_csv.py
│   ├── crear_gold_bachilleres_empresas.py
│   ├── inspeccionar_p3.py
│   ├── listar_tablas_mineduc.py
│   ├── inspeccionar_mineduc_csv.py
│   ├── buscar_fuente_mineduc.py
│   └── inspeccionar_mineduc_inicio.py
│
├── pipeline.py
├── requirements.txt
└── README.md
```

---

## 7. Requisitos

- Python 3.13
- pandas
- openpyxl
- SQLite
- Power BI Desktop
- Power Automate Desktop
- Visual Studio Code

Instalar dependencias:

```powershell
pip install pandas openpyxl
```

---

## 8. Ejecución del pipeline

Desde la carpeta principal del proyecto:

```powershell
cd "C:\Users\A S U S\OneDrive\Documentos\reto_macroentorno"
```

Ejecutar:

```powershell
& "C:\Users\A S U S\AppData\Local\Programs\Python\Python313\python.exe" ".\pipeline.py"
```

El pipeline ejecuta cinco pasos:

1. Procesar archivos SQL de RPA.
2. Transformar datos de SUPERCIAS.
3. Crear tablas Gold de SUPERCIAS.
4. Exportar tablas Gold de SUPERCIAS a CSV.
5. Crear la tabla Gold de estudiantes y empresas.

El resultado esperado es:

```text
PIPELINE COMPLETADO CORRECTAMENTE
```

---

## 9. Resultados principales del pipeline

En la última ejecución se obtuvieron los siguientes resultados:

- 1.950.119 registros almacenados en SQLite.
- 219.754 empresas únicas en el directorio.
- 1.672.590 registros financieros procesados.
- 1.345.488 registros financieros con provincia.
- 24 provincias en `gold_empresas_provincia`.
- 25 filas en `gold_bachilleres_vs_empresas`.
- 4.059.992 estudiantes de educación ordinaria.
- 179.447 empresas activas.

Principales provincias con mayor ratio de estudiantes por empresa:

- Esmeraldas.
- Bolívar.
- Los Ríos.
- Carchi.
- Morona Santiago.
- Napo.
- Pastaza.
- Manabí.
- Chimborazo.
- Cotopaxi.

---

## 10. Integración con RPA

El flujo de RPA descarga y deposita los archivos en la estructura del proyecto. El pipeline de datos procesa los archivos recibidos y actualiza la base SQLite y los archivos Gold.

Archivos principales procesados:

```text
tab_consolidado_export.sql
tab_consolidado_supercias.sql
```

Formato recomendado para nuevas entregas:

```text
fuente_YYYYMMDD.extension
```

Ejemplos:

```text
supercias_directorio_20260722.sql
supercias_ranking_20260722.sql
```

Responsabilidades:

### Equipo RPA

- Descargar archivos.
- Mantener nombres y formatos acordados.
- Depositar archivos en la carpeta definida.
- Informar cuando exista una nueva descarga.

### Equipo de Datos

- Validar estructura.
- Procesar archivos.
- Transformar y cargar datos.
- Generar tablas Gold.
- Actualizar archivos CSV.
- Verificar el dashboard.

---

## 11. Actualización del dashboard

Después de ejecutar el pipeline:

1. Abrir Power BI.
2. Seleccionar `Inicio`.
3. Pulsar `Actualizar`.
4. Verificar que no existan errores.
5. Guardar el archivo PBIX.

Archivo recomendado:

```text
RetMacro_Final_Rodrigo.pbix
```

Power BI utiliza principalmente archivos CSV generados en las carpetas:

```text
gold/
gold/supercias/
powerbi_csv/
```

---

## 12. Descripción de las páginas del dashboard

### Página 1 — Evolución económica

Visualizaciones:

- Línea de evolución del PIB per cápita nominal.
- Barras de variación anual del PIB.
- Clasificación de crecimiento o contracción.
- KPI de PIB per cápita más reciente.
- KPI de variación interanual más reciente.
- Línea del IEE del último año.

Hallazgo:

La economía ecuatoriana presenta una tendencia de crecimiento de largo plazo, aunque existen años de contracción y recuperación. El PIB per cápita y la variación anual permiten identificar los principales cambios económicos.

### Página 2 — Actividad económica y empleo

Visualizaciones:

- VAB por provincia.
- Indicadores nacionales de empleo.
- Top 10 sectores CIIU por VAB.
- KPI de desempleo reciente.

Hallazgo:

La actividad económica se concentra en determinadas provincias y sectores. Los indicadores laborales permiten observar diferencias entre empleo, subempleo y desempleo.

### Página 3 — Demanda educativa y empresas

Visualizaciones:

- Gráfico combinado de estudiantes y empresas activas.
- Top 10 provincias por ratio de estudiantes por empresa.
- Tarjeta de estudiantes.
- Tarjeta de empresas.
- Tarjeta de ratio nacional.
- Tabla comparativa territorial.
- Filtro por provincia.

Hallazgo:

Esmeraldas, Bolívar y Los Ríos presentan una mayor concentración de estudiantes por empresa activa. Estos territorios pueden representar oportunidades estratégicas para fortalecer acciones de difusión, captación y oferta educativa de la UTPL.

---

## 13. Decisiones de limpieza

Principales decisiones aplicadas:

- Conversión de campos numéricos con `pd.to_numeric()`.
- Normalización de nombres de provincias.
- Eliminación de tildes para facilitar cruces.
- Conversión de texto a mayúsculas.
- Eliminación de espacios innecesarios.
- Filtrado de empresas con situación legal `ACTIVA`.
- Conteo de empresas usando RUC distinto.
- Uso del último año lectivo disponible de MINEDUC.
- Filtrado de `Tipo_Educacion = ORDINARIO`.
- Tratamiento de divisiones por cero con valores nulos.
- Redondeo del ratio a dos decimales.
- Exportación de CSV con codificación `utf-8-sig`.

---

## 14. Limitaciones

- La fuente MINEDUC utilizada no contiene detalle por grado o curso.
- El indicador de la Página 3 utiliza estudiantes de educación ordinaria como aproximación.
- Algunos análisis de empleo sectorial se representan mediante VAB por CIIU cuando no existe el detalle completo de personas ocupadas.
- La base de datos actual utiliza SQLite, acorde con el alcance de cuarto ciclo.
- Los archivos de origen pueden cambiar de nombre o estructura, por lo que deben mantenerse los acuerdos con el equipo RPA.

---

## 15. Evidencias recomendadas

Para la entrega se deben incluir:

- Captura de la Página 1.
- Captura de la Página 2.
- Captura de la Página 3.
- Captura de `PIPELINE COMPLETADO CORRECTAMENTE`.
- Captura del flujo RPA.
- Captura de la carpeta `gold`.
- Captura de las tablas SQLite.
- Captura de Power BI después de actualizar.

---

## 16. Demostración

Orden sugerido para la demostración:

1. Presentar el objetivo.
2. Mostrar la arquitectura.
3. Mostrar las fuentes.
4. Ejecutar la automatización RPA.
5. Ejecutar `pipeline.py`.
6. Mostrar la creación de tablas Gold.
7. Actualizar Power BI.
8. Explicar las tres páginas.
9. Presentar los hallazgos.
10. Mencionar limitaciones y conclusiones.

---

## 17. Autor

**Rodrigo Seraquive**

Proyecto académico de Ingeniería en Computación — UTPL.

---

## 18. Estado del proyecto

- Pipeline: funcionando.
- Integración con RPA: funcionando.
- Base SQLite: funcionando.
- Tablas Gold: generadas.
- Exportación CSV: funcionando.
- Dashboard Power BI: actualizado.
- Página 1: completada.
- Página 2: completada.
- Página 3: completada.
