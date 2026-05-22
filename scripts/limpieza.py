import pandas as pd

print("Cargando dataset...")

# Leer archivo Excel
df = pd.read_excel(
    'datos/registro-administrativo-historico_2009-2024-inicio.xlsx',
    sheet_name=0,
    engine='openpyxl'
)

print("Dataset cargado correctamente")

# ============================================= =====
# RENOMBRAR COLUMNAS
# ==================================================

RENAME = {
    'Periodo': 'anio_lectivo',
    'Codigo_Institucion': 'cod_amie',
    'Nombre_Institucion': 'nombre_institucion',
    'Provincia': 'provincia',
    'Canton': 'canton',
    'Parroquia': 'parroquia',
    'Sostenimiento': 'sostenimiento',
    'Area': 'area',
    'Modallidad': 'modalidad',
    'Jornada': 'jornada',
    'Total_Docentes': 'total_docentes',
    'Total_Estudiantes': 'total_estudiantes',
    'Estudiantes_Femenino': 'estudiantes_f',
    'Estudiantes_Masculino': 'estudiantes_m',
    'Nivel_educativo': 'nivel_educacion'
}

df = df.rename(columns=RENAME)

print("\nColumnas renombradas correctamente")

# ==================================================
# LIMPIEZA DE NULOS
# ==================================================

nums = [
    'total_docentes',
    'total_estudiantes',
    'estudiantes_f',
    'estudiantes_m'
]

# Verificar columnas existentes
nums_existentes = [col for col in nums if col in df.columns]

df[nums_existentes] = df[nums_existentes].fillna(0)

print("\nValores nulos reemplazados con 0")

# ==================================================
# ELIMINAR DUPLICADOS
# ==================================================

antes = len(df)

if 'cod_amie' in df.columns and 'anio_lectivo' in df.columns:
    df = df.drop_duplicates(subset=['cod_amie', 'anio_lectivo'])

despues = len(df)

print(f"\nDuplicados eliminados: {antes - despues}")

# ==================================================
# VALIDAR CONSISTENCIA
# ==================================================

if (
    'total_estudiantes' in df.columns and
    'estudiantes_f' in df.columns and
    'estudiantes_m' in df.columns
):

    inconsistentes = df[
        df['total_estudiantes'] !=
        (df['estudiantes_f'] + df['estudiantes_m'])
    ]

    print(f"\nRegistros inconsistentes encontrados: {len(inconsistentes)}")

# ==================================================
# GUARDAR DATASET LIMPIO
# ==================================================

df.to_csv(
    'datos/dataset_limpio.csv',
    index=False,
    encoding='utf-8'
)

print("\nDataset limpio guardado correctamente")