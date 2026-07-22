import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "macroentorno.db"

INDICADORES = [
    "SUPERCIAS_DIRECTORIO",
    "SUPERCIAS_RANKING",
]


def decodificar_json(texto):
    datos = texto

    for _ in range(5):
        if not isinstance(datos, str):
            break

        datos = datos.strip()

        try:
            datos = json.loads(datos)
        except json.JSONDecodeError:
            break

    return datos


def mostrar_muestra(conexion, indicador):
    fila = conexion.execute(
        """
        SELECT dato_clave, datos_json
        FROM raw_supercias_consolidado
        WHERE indicador = ?
          AND datos_json IS NOT NULL
        LIMIT 1
        """,
        (indicador,),
    ).fetchone()

    print()
    print("=" * 70)
    print(indicador)
    print("=" * 70)

    if fila is None:
        print("No se encontraron registros.")
        return

    dato_clave, texto_json = fila
    datos = decodificar_json(texto_json)

    print(f"Dato clave: {dato_clave}")
    print(f"Tipo obtenido: {type(datos).__name__}")
    print()

    if isinstance(datos, dict):
        print(f"Cantidad de campos: {len(datos)}")
        print()

        for clave, valor in datos.items():
            print(f"{clave}: {valor}")

    elif isinstance(datos, list):
        print(f"Cantidad de elementos: {len(datos)}")
        print()

        if datos:
            primer_elemento = datos[0]

            if isinstance(primer_elemento, dict):
                print("Campos del primer elemento:")
                print()

                for clave, valor in primer_elemento.items():
                    print(f"{clave}: {valor}")
            else:
                print(primer_elemento)

    else:
        print("No se pudo convertir el contenido en diccionario o lista.")
        print()
        print(str(datos)[:1000])


def main():
    print(f"Base de datos: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conexion:
        for indicador in INDICADORES:
            mostrar_muestra(conexion, indicador)


if __name__ == "__main__":
    main()