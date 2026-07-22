import pandas as pd

RUTA = "data_raw/mineduc/"

def limpiar_mineduc():
    archivo = RUTA + "2Registro-Administrativo-Historico_2009-2024-Fin.xlsx"
    df = pd.read_excel(archivo)
    df = df.rename(columns={
        "Año_lectivo": "anio_lectivo",
        "AMIE": "amie",
        "Nombre_Institucion": "institucion",
        "Zona": "zona",
        "Provincia": "provincia",
        "Cod_Provincia": "cod_provincia",
        "Canton": "canton",
        "Cod_Canton": "cod_canton",
        "Parroquia": "parroquia",
        "Cod_Parroquia": "cod_parroquia",
        "Escolarizacion": "escolarizacion",
        "Tipo_Educacion": "tipo_educacion",
        "Sostenimiento": "sostenimiento",
        "Área": "area",
        "Regimen_Escolar": "regimen_escolar",
        "Jurisdiccion": "jurisdiccion",
        "Modalidad": "modalidad",
        "Jornada": "jornada",
        "Acceso_Edificio": "acceso_edificio",
        "Total_Estudiantes": "total_estudiantes",
        "Promovidos": "promovidos",
        "No promovidos": "no_promovidos",
        "Abandono": "abandono",
    })
    df["anio"] = df["anio_lectivo"].astype(str).str.extract(r"(\d{4})").astype(int)
    df["provincia"] = df["provincia"].astype(str).str.strip().str.upper()
    for col in ["total_estudiantes", "promovidos", "no_promovidos", "abandono"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["amie", "anio"])
    return df

if __name__ == "__main__":
    df = limpiar_mineduc()
    print(df.head())
    print(df.shape)
    print(df["anio"].min(), "-", df["anio"].max())