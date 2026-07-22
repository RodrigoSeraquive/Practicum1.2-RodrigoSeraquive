import pandas as pd

RUTA = "data_raw/bce/"

def limpiar_pib_real():
    df = pd.read_csv(RUTA + "crecimiento-anual-pib.csv")
    df = df.rename(columns={
        "Período": "anio",
        "Crecimiento Anual PIB en Porcentaje": "variacion_pib_pct"
    })
    # El año puede venir como número (1980) o como texto ("1980" o "1980-12-31")
    # Esto extrae los primeros 4 dígitos y los convierte a entero sin importar el formato
    df["anio"] = df["anio"].astype(str).str.extract(r"(\d{4})").astype(int)
    df["variacion_pib_pct"] = pd.to_numeric(df["variacion_pib_pct"], errors="coerce")
    # No tenemos PIB en musd, población ni PIB per cápita en este archivo:
    # se quedan como columnas vacías por ahora, es correcto dejarlas en NULL
    df["pib_real_musd"] = None
    df["poblacion"] = None
    df["pib_percapita"] = None
    df = df.drop_duplicates(subset="anio").sort_values("anio")
    return df

def limpiar_pib_percapita_nominal():
    df = pd.read_csv(RUTA + "pib-per-cpita-nominal.csv")
    df = df.rename(columns={
        "Período": "periodo",
        "PIB Per Cápita Nominal en USD": "pib_percapita_nominal"
    })
    df["periodo"] = pd.to_datetime(df["periodo"], errors="coerce")
    df["anio"] = df["periodo"].dt.year
    df["pib_percapita_nominal"] = pd.to_numeric(df["pib_percapita_nominal"], errors="coerce")
    df = df.drop_duplicates(subset="anio")
    return df

def limpiar_petroleo_riesgo():
    df = pd.read_csv(RUTA + "precio-petrleo-wti.csv")
    df = df.rename(columns={
        "Período": "fecha",
        "Precio Petróleo (WTI) en USD por barril": "precio_petroleo_wti"
    })
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["precio_petroleo_wti"] = pd.to_numeric(df["precio_petroleo_wti"], errors="coerce")
    # Este archivo no trae riesgo país; se deja NULL y se documenta
    df["riesgo_pais_pb"] = None
    df = df.dropna(subset=["fecha"]).drop_duplicates(subset="fecha")
    return df

def limpiar_iee():
    df = pd.read_csv(RUTA + "figura-1-ndice-de-expect.csv")
    df = df.rename(columns={
        "DateTime": "fecha",
        "IEE": "iee_global"
    })
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["iee_global"] = pd.to_numeric(df["iee_global"], errors="coerce")
    # Este archivo no trae desglose por sector; se deja NULL y se documenta
    df["comercio"] = None
    df["construccion"] = None
    df["manufactura"] = None
    df = df.dropna(subset=["fecha"]).drop_duplicates(subset="fecha")
    return df

def limpiar_vab():
    archivo = RUTA + "CtasProv2007-2020.xlsx"
    hojas_vab = [h for h in pd.ExcelFile(archivo).sheet_names if h.startswith("VAB_")]
    todas = []
    for hoja in hojas_vab:
        anio = 2000 + int(hoja.split("_")[1])  # VAB_20 -> 2020, VAB_07 -> 2007
        raw = pd.read_excel(archivo, sheet_name=hoja, header=None)
        fila_codigos = raw.iloc[15]
        # columnas de CIIU: desde la columna 2, donde el código no es nulo (excluye la última col de total)
        cols_ciiu = [c for c in range(2, raw.shape[1]) if pd.notna(fila_codigos[c])]
        codigos = {c: str(fila_codigos[c]) for c in cols_ciiu}
        # filas de provincia: desde la fila 18, mientras col0 (número) y col1 (nombre) tengan datos
        filas_provincia = []
        fila = 18
        while fila < raw.shape[0]:
            if pd.isna(raw.iloc[fila, 0]) or pd.isna(raw.iloc[fila, 1]):
                break
            filas_provincia.append(fila)
            fila += 1
        tabla = raw.iloc[filas_provincia, [1] + cols_ciiu].copy()
        tabla.columns = ["provincia"] + [codigos[c] for c in cols_ciiu]
        largo = tabla.melt(id_vars="provincia", var_name="ciiu", value_name="vab_miles_usd")
        largo["anio"] = anio
        todas.append(largo)
    df = pd.concat(todas, ignore_index=True)
    df["provincia"] = df["provincia"].astype(str).str.strip().str.upper()
    df["vab_miles_usd"] = pd.to_numeric(df["vab_miles_usd"], errors="coerce")
    df = df.dropna(subset=["vab_miles_usd", "provincia"])
    return df

if __name__ == "__main__":
    print(limpiar_pib_real().head())
    print(limpiar_pib_percapita_nominal().head())
    print(limpiar_petroleo_riesgo().head())
    print(limpiar_iee().head())
    print(limpiar_vab().head())