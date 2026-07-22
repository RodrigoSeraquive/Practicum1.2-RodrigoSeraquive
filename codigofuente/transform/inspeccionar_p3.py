import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "macroentorno.db"

TABLAS = [
    "fact_mineduc_bachilleres",
    "fact_empresas_rpa",
]


def mostrar_columnas(conexion, tabla):
    print()
    print("=" * 80)
    print(f"COLUMNAS DE: {tabla}")
    print("=" * 80)

    columnas = conexion.execute(
        f"PRAGMA table_info({tabla})"
    ).fetchall()

    if not columnas:
        print("La tabla no existe o no tiene columnas.")
        return []

    nombres = []

    for columna in columnas:
        nombre = columna[1]
        tipo = columna[2]

        nombres.append(nombre)
        print(f"{nombre} | {tipo}")

    return nombres


def mostrar_muestra(conexion, tabla):
    print()
    print("=" * 80)
    print(f"MUESTRA DE: {tabla}")
    print("=" * 80)

    try:
        filas = conexion.execute(
            f"SELECT * FROM {tabla} LIMIT 3"
        ).fetchall()

        for fila in filas:
            print(fila)

    except sqlite3.Error as error:
        print(f"ERROR: {error}")


def buscar_columnas_importantes(columnas):
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
        "periodo",
        "sostenimiento",
    ]

    encontradas = []

    for columna in columnas:
        columna_minuscula = columna.lower()

        if any(palabra in columna_minuscula for palabra in palabras):
            encontradas.append(columna)

    return encontradas


def mostrar_valores_distintos(conexion, tabla, columnas):
    print()
    print("=" * 80)
    print(f"VALORES DISTINTOS IMPORTANTES DE: {tabla}")
    print("=" * 80)

    for columna in columnas:
        try:
            valores = conexion.execute(
                f"""
                SELECT DISTINCT "{columna}"
                FROM {tabla}
                WHERE "{columna}" IS NOT NULL
                LIMIT 30
                """
            ).fetchall()

            print()
            print(f"{columna}:")

            for valor in valores:
                print(f"  {valor[0]}")

        except sqlite3.Error as error:
            print(f"ERROR en {columna}: {error}")


def main():
    if not DB_PATH.exists():
        print(f"ERROR: no existe la base de datos:")
        print(DB_PATH)
        raise SystemExit(1)

    print(f"Base de datos: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conexion:
        for tabla in TABLAS:
            columnas = mostrar_columnas(conexion, tabla)
            mostrar_muestra(conexion, tabla)

            importantes = buscar_columnas_importantes(columnas)
            mostrar_valores_distintos(
                conexion,
                tabla,
                importantes,
            )


if __name__ == "__main__":
    main()