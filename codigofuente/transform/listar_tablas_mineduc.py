import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "macroentorno.db"


def main():
    print(f"Base de datos: {DB_PATH}")
    print()

    with sqlite3.connect(DB_PATH) as conexion:
        tablas = conexion.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type IN ('table', 'view')
            ORDER BY name
        """).fetchall()

        print("=" * 70)
        print("TABLAS Y VISTAS DISPONIBLES")
        print("=" * 70)

        encontradas = []

        for (nombre,) in tablas:
            print(nombre)

            nombre_min = nombre.lower()

            if any(
                palabra in nombre_min
                for palabra in ["mineduc", "amie", "bachiller", "educacion"]
            ):
                encontradas.append(nombre)

        print()
        print("=" * 70)
        print("POSIBLES TABLAS DE MINEDUC")
        print("=" * 70)

        if encontradas:
            for nombre in encontradas:
                print(nombre)
        else:
            print("No se encontró ninguna tabla relacionada con MINEDUC.")


if __name__ == "__main__":
    main()