from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
CARPETA = BASE_DIR / "data_raw" / "mineduc"


def buscar_csv():
    archivos = list(CARPETA.glob("*inicio*.csv"))

    if not archivos:
        print("No se encontró el CSV de inicio.")
        raise SystemExit(1)

    return archivos[0]


def main():
    ruta = buscar_csv()

    print("Archivo encontrado:")
    print(ruta)

    intentos = [
        {"sep": ";", "encoding": "latin-1"},
        {"sep": ";", "encoding": "utf-8-sig"},
        {"sep": ",", "encoding": "latin-1"},
        {"sep": ",", "encoding": "utf-8-sig"},
    ]

    df = None

    for configuracion in intentos:
        try:
            df = pd.read_csv(
                ruta,
                nrows=10,
                low_memory=False,
                **configuracion
            )

            if len(df.columns) > 1:
                print()
                print("Configuración correcta:")
                print(configuracion)
                break

        except Exception:
            continue

    if df is None or len(df.columns) <= 1:
        print("No se pudo leer correctamente el archivo.")
        raise SystemExit(1)

    print()
    print("=" * 80)
    print("COLUMNAS")
    print("=" * 80)

    for columna in df.columns:
        print(columna)

    print()
    print("=" * 80)
    print("PRIMERAS FILAS")
    print("=" * 80)
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()