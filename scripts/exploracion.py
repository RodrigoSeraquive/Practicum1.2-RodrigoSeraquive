import pandas as pd

print("Cargando dataset histórico...")

# Leer archivo Excel
df = pd.read_excel(
    'datos/registro-administrativo-historico_2009-2024-inicio.xlsx',
    sheet_name=0,
    engine='openpyxl'
)

print("\n========== DIMENSIONES ==========")
print(df.shape)

print("\n========== PRIMERAS FILAS ==========")
print(df.head())

print("\n========== COLUMNAS ==========")
print(df.columns)

print("\n========== TIPOS DE DATOS ==========")
print(df.dtypes)

print("\n========== VALORES NULOS ==========")
print(df.isnull().sum().sort_values(ascending=False).head(20))

# Verificar si existen columnas importantes
if 'Sostenimiento' in df.columns:
    print("\n========== SOSTENIMIENTO ==========")
    print(df['Sostenimiento'].value_counts())

if 'Nivel Educacion' in df.columns:
    print("\n========== NIVEL EDUCACION ==========")
    print(df['Nivel Educacion'].value_counts())