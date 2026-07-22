import pandas as pd
import unicodedata

def limpiar_empresas():

    archivo = "data_raw/supercias/directorio_companias.xlsx"

    df = pd.read_excel(
        archivo,
        header=4
    )

    df.columns = [
        unicodedata.normalize("NFKD", str(c))
        .encode("ascii", "ignore")
        .decode("utf-8")
        .strip()
        .lower()
        .replace(" ", "_")
        for c in df.columns
    ]

    df = df.dropna(how="all")

    fact = pd.DataFrame()

    fact["id"] = range(1, len(df)+1)

    fact["provincia"] = (
        df["provincia"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    fact["ruc"] = df["ruc"]

    fact["situacion_legal"] = df["situacion_legal"]

    return fact