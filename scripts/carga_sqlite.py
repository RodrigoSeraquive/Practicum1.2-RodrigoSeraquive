import pandas as pd
from sqlalchemy import create_engine

print("Cargando dataset limpio...")

# Leer dataset limpio
df = pd.read_csv(
    'datos/dataset_limpio.csv',
    low_memory=False
)

print("Dataset cargado correctamente")

# ==================================================
# CREAR BASE SQLITE
# ==================================================

engine = create_engine('sqlite:///base_datos/amie_mineduc.db')

print("Base SQLite creada correctamente")

# ==================================================
# GUARDAR TABLA
# ==================================================

df.to_sql(
    'instituciones',
    engine,
    if_exists='replace',
    index=False
)

print("Tabla instituciones creada correctamente")

# ==================================================
# CONSULTA DE VERIFICACION
# ==================================================

consulta = pd.read_sql(
    "SELECT COUNT(*) AS total_registros FROM instituciones",
    engine
)

print("\nTOTAL DE REGISTROS")
print(consulta)

print("\nProceso finalizado correctamente")