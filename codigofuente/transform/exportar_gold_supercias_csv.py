import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "macroentorno.db"
GOLD_DIR = BASE_DIR / "gold" / "supercias"


TABLAS = [
    "gold_empresas_provincia",
    "gold_empresas_situacion",
    "gold_empresas_ciiu",
    "gold_ranking_provincia_anio",
    "gold_ranking_ciiu_anio",
    "gold_resumen_supercias",
]


def exportar_tabla(conexion: sqlite3.Connection, tabla: str) -> None:
    consulta = f"SELECT * FROM {tabla}"
    dataframe = pd.read_sql_query(consulta, conexion)

    ruta_salida = GOLD_DIR / f"{tabla}.csv"

    dataframe.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8-sig",
        sep=",",
    )

    print(f"{tabla}: {len(dataframe):,} filas")
    print(f"Archivo: {ruta_salida}")
    print()


def main() -> None:
    if not DB_PATH.exists():
        print(f"ERROR: no existe la base de datos: {DB_PATH}")
        raise SystemExit(1)

    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 75)
    print("EXPORTACIÓN DE TABLAS GOLD DE SUPERCIAS A CSV")
    print("=" * 75)
    print(f"Base de datos: {DB_PATH}")
    print(f"Carpeta de salida: {GOLD_DIR}")
    print()

    with sqlite3.connect(DB_PATH) as conexion:
        for tabla in TABLAS:
            exportar_tabla(conexion, tabla)

    print("=" * 75)
    print("ARCHIVOS CSV EXPORTADOS CORRECTAMENTE")
    print("=" * 75)


if __name__ == "__main__":
    main()