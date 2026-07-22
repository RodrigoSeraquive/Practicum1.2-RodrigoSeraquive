from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

CSV_MINEDUC = (
    BASE_DIR
    / "powerbi_csv"
    / "fact_mineduc_bachilleres.csv"
)


def main():
    if not CSV_MINEDUC.exists():
        print("ERROR: no existe el archivo:")
        print(CSV_MINEDUC)
        raise SystemExit(1)

    print("=" * 80)
    print("ARCHIVO MINEDUC")
    print("=" * 80)
    print(CSV_MINEDUC)

    df = pd.read_csv(
        CSV_MINEDUC,
        encoding="utf-8-sig",
        low_memory=False,
    )

    print()
    print("=" * 80)
    print("TOTAL DE FILAS Y COLUMNAS")
    print("=" * 80)
    print(f"Filas: {len(df):,}")
    print(f"Columnas: {len(df.columns)}")

    print()
    print("=" * 80)
    print("NOMBRES DE COLUMNAS")
    print("=" * 80)

    for columna in df.columns:
        print(columna)

    print()
    print("=" * 80)
    print("PRIMERAS 3 FILAS")
    print("=" * 80)
    print(df.head(3).to_string())

    palabras = [
        "provincia",
        "grado",
        "curso",
        "nivel",
        "bachiller",
        "estudiante",
        "alumno",
        "matricula",
        "total",
        "anio",
        "año",
        "periodo",
    ]

    columnas_importantes = [
        columna
        for columna in df.columns
        if any(
            palabra in columna.lower()
            for palabra in palabras
        )
    ]

    print()
    print("=" * 80)
    print("COLUMNAS IMPORTANTES ENCONTRADAS")
    print("=" * 80)

    for columna in columnas_importantes:
        print()
        print(f"--- {columna} ---")

        valores = (
            df[columna]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .head(30)
            .tolist()
        )

        for valor in valores:
            print(valor)


if __name__ == "__main__":
    main()