from pathlib import Path
import sqlite3
import unicodedata

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

CSV_MINEDUC = (
    BASE_DIR
    / "data_raw"
    / "mineduc"
    / "amie_2009_2024_inicio.csv"
)

DB_PATH = BASE_DIR / "db" / "macroentorno.db"

GOLD_DIR = BASE_DIR / "gold"
CSV_SALIDA = GOLD_DIR / "gold_bachilleres_vs_empresas.csv"

TABLA_EMPRESAS = "fact_empresas_rpa"
TABLA_GOLD = "gold_bachilleres_vs_empresas"


def normalizar_texto(valor):
    if pd.isna(valor):
        return None

    texto = str(valor).strip().upper()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    reemplazos = {
        "LOS RIOS": "LOS RIOS",
        "MANABI": "MANABI",
        "BOLIVAR": "BOLIVAR",
        "CANAR": "CANAR",
        "GALAPAGOS": "GALAPAGOS",
        "SANTO DOMINGO DE LOS TSACHILAS":
            "SANTO DOMINGO DE LOS TSACHILAS",
    }

    return reemplazos.get(texto, texto)


def verificar_archivos():
    if not CSV_MINEDUC.exists():
        raise FileNotFoundError(
            f"No existe el archivo MINEDUC:\n{CSV_MINEDUC}"
        )

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"No existe la base de datos:\n{DB_PATH}"
        )


def leer_mineduc():
    print("Leyendo MINEDUC...")

    df = pd.read_csv(
        CSV_MINEDUC,
        sep=";",
        encoding="latin-1",
        low_memory=False,
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.replace("ï»¿", "", regex=False)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    columnas_necesarias = [
        "Anio_lectivo",
        "Provincia",
        "Tipo_Educacion",
        "Total_Estudiantes",
    ]

    faltantes = [
        columna
        for columna in columnas_necesarias
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan estas columnas en el archivo MINEDUC: "
            + ", ".join(faltantes)
        )

    df["Provincia"] = df["Provincia"].apply(normalizar_texto)

    df["Tipo_Educacion"] = (
        df["Tipo_Educacion"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["Total_Estudiantes"] = pd.to_numeric(
        df["Total_Estudiantes"],
        errors="coerce",
    ).fillna(0)

    df["Anio_lectivo"] = (
        df["Anio_lectivo"]
        .astype(str)
        .str.strip()
    )

    ultimo_anio = (
        df["Anio_lectivo"]
        .dropna()
        .sort_values()
        .iloc[-1]
    )

    print(f"Último año lectivo encontrado: {ultimo_anio}")

    filtrado = df[
        (df["Anio_lectivo"] == ultimo_anio)
        & (df["Tipo_Educacion"] == "ORDINARIO")
        & (df["Provincia"].notna())
    ].copy()

    resumen = (
        filtrado.groupby(
            ["Anio_lectivo", "Provincia"],
            as_index=False,
        )["Total_Estudiantes"]
        .sum()
        .rename(
            columns={
                "Anio_lectivo": "anio_lectivo",
                "Provincia": "provincia",
                "Total_Estudiantes":
                    "total_estudiantes_ordinaria",
            }
        )
    )

    resumen["total_estudiantes_ordinaria"] = (
        resumen["total_estudiantes_ordinaria"]
        .round(0)
        .astype(int)
    )

    return resumen


def verificar_tabla_empresas(conexion):
    resultado = conexion.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (TABLA_EMPRESAS,),
    ).fetchone()

    if resultado is None:
        raise ValueError(
            f"No existe la tabla {TABLA_EMPRESAS} "
            f"en {DB_PATH}"
        )


def leer_empresas():
    print("Leyendo empresas activas...")

    with sqlite3.connect(DB_PATH) as conexion:
        verificar_tabla_empresas(conexion)

        df = pd.read_sql_query(
            f"""
            SELECT
                provincia,
                COUNT(DISTINCT ruc) AS empresas_activas
            FROM {TABLA_EMPRESAS}
            WHERE UPPER(TRIM(situacion_legal)) = 'ACTIVA'
              AND provincia IS NOT NULL
              AND TRIM(provincia) <> ''
            GROUP BY provincia
            """,
            conexion,
        )

    df["provincia"] = df["provincia"].apply(normalizar_texto)

    df["empresas_activas"] = pd.to_numeric(
        df["empresas_activas"],
        errors="coerce",
    ).fillna(0).astype(int)

    df = (
        df.groupby(
            "provincia",
            as_index=False,
        )["empresas_activas"]
        .sum()
    )

    return df


def crear_gold():
    verificar_archivos()

    mineduc = leer_mineduc()
    empresas = leer_empresas()

    gold = mineduc.merge(
        empresas,
        on="provincia",
        how="left",
    )

    gold["empresas_activas"] = (
        gold["empresas_activas"]
        .fillna(0)
        .astype(int)
    )

    denominador = (
        gold["empresas_activas"]
        .replace(0, float("nan"))
        .astype(float)
    )

    gold["ratio_estudiantes_empresa"] = (
        gold["total_estudiantes_ordinaria"]
        .astype(float)
        .div(denominador)
        .round(2)
    )

    gold = gold[
        [
            "anio_lectivo",
            "provincia",
            "total_estudiantes_ordinaria",
            "empresas_activas",
            "ratio_estudiantes_empresa",
        ]
    ]

    gold = gold.sort_values(
        by="ratio_estudiantes_empresa",
        ascending=False,
        na_position="last",
    ).reset_index(drop=True)

    GOLD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    gold.to_csv(
        CSV_SALIDA,
        index=False,
        encoding="utf-8-sig",
    )

    with sqlite3.connect(DB_PATH) as conexion:
        gold.to_sql(
            TABLA_GOLD,
            conexion,
            if_exists="replace",
            index=False,
        )

    print()
    print("=" * 80)
    print("GOLD CREADO CORRECTAMENTE")
    print("=" * 80)
    print(f"Filas generadas: {len(gold)}")
    print(f"CSV generado: {CSV_SALIDA}")
    print(f"Tabla creada: {TABLA_GOLD}")
    print()

    print("Primeras 10 filas:")
    print(gold.head(10).to_string(index=False))

    print()
    print("Totales:")
    print(
        "Estudiantes de educación ordinaria:",
        f"{gold['total_estudiantes_ordinaria'].sum():,}",
    )
    print(
        "Empresas activas:",
        f"{gold['empresas_activas'].sum():,}",
    )


if __name__ == "__main__":
    try:
        crear_gold()

    except Exception as error:
        print()
        print("=" * 80)
        print("ERROR AL CREAR EL GOLD")
        print("=" * 80)
        print(error)
        raise