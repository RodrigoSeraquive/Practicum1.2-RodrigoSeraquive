import pandas as pd


def limpiar_empleo():

    archivo = "data_raw/inec/2. Tasas.csv"


    df = pd.read_csv(
        archivo,
        sep=";",
        skiprows=2,
        encoding="latin1",
        header=None
    )


    df = df.iloc[:, :8]


    df.columns = [
        "encuesta",
        "periodo",
        "indicador",
        "valor_nacional",
        "urbana",
        "rural",
        "hombre",
        "mujer"
    ]


    df = df.dropna(
        subset=["periodo"]
    )


    df["valor_nacional"] = (
        df["valor_nacional"]
        .astype(str)
        .str.replace(",", ".")
    )


    df["valor_nacional"] = pd.to_numeric(
        df["valor_nacional"],
        errors="coerce"
    )


    df = df.dropna(
        subset=["valor_nacional"]
    )


    df = df[
        [
            "periodo",
            "indicador",
            "valor_nacional"
        ]
    ]


    return df