import pandas as pd
from sqlalchemy import create_engine

# Conectar SQLite
engine = create_engine('sqlite:///base_datos/amie_mineduc.db')

print("Conexión SQLite exitosa")

# ==================================================
# P1
# MATRICULA POR PROVINCIA
# ==================================================

print("\n========== P1 ==========")

p1 = pd.read_sql("""

SELECT
    provincia,
    SUM(total_estudiantes) AS total_matricula
FROM instituciones
GROUP BY provincia
ORDER BY total_matricula DESC

""", engine)

print(p1.head(10))

# ==================================================
# P2
# SOSTENIMIENTO EN LOJA
# ==================================================

print("\n========== P2 ==========")

p2 = pd.read_sql("""

SELECT
    area,
    sostenimiento,
    COUNT(cod_amie) AS total_instituciones
FROM instituciones
WHERE provincia = 'LOJA'
GROUP BY area, sostenimiento
ORDER BY area

""", engine)

print(p2)

# ==================================================
# P3
# EVOLUCION INSTITUCIONES
# ==================================================

print("\n========== P3 ==========")

p3 = pd.read_sql("""

SELECT
    anio_lectivo,
    COUNT(cod_amie) AS total_instituciones
FROM instituciones
GROUP BY anio_lectivo
ORDER BY anio_lectivo

""", engine)

print(p3)

print("\nConsultas ejecutadas correctamente")