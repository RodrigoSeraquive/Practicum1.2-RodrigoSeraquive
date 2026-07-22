from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

EXTENSIONES = {
    ".csv",
    ".xlsx",
    ".xls",
}

PALABRAS_ARCHIVO = [
    "mineduc",
    "amie",
    "bachiller",
    "educacion",
    "estudiante",
    "matricula",
]


def es_archivo_relevante(ruta: Path) -> bool:
    nombre = ruta.name.lower()
    ruta_completa = str(ruta).lower()

    return (
        ruta.suffix.lower() in EXTENSIONES
        and any(
            palabra in nombre or palabra in ruta_completa
            for palabra in PALABRAS_ARCHIVO
        )
    )


def leer_csv(ruta: Path):
    intentos = [
        {"encoding": "utf-8-sig", "sep": None},
        {"encoding": "latin-1", "sep": None},
        {"encoding": "utf-8-sig", "sep": ";"},
        {"encoding": "latin-1", "sep": ";"},
        {"encoding": "utf-8-sig", "sep": ","},
        {"encoding": "latin-1", "sep": ","},
    ]

    for configuracion in intentos:
        try:
            return pd.read_csv(
                ruta,
                nrows=5,
                low_memory=False,
                engine="python",
                **configuracion,
            )
        except Exception:
            continue

    return None


def inspeccionar_csv(ruta: Path):
    df = leer_csv(ruta)

    if df is None:
        print("No se pudo leer el CSV.")
        return

    print("Columnas encontradas:")

    for columna in df.columns:
        print(f"  - {columna}")

    print()
    print("Primera fila:")

    if not df.empty:
        print(df.head(1).to_string(index=False))


def inspeccionar_excel(ruta: Path):
    try:
        archivo_excel = pd.ExcelFile(ruta)
    except Exception as error:
        print(f"No se pudo abrir el Excel: {error}")
        return

    print("Hojas encontradas:")

    for hoja in archivo_excel.sheet_names[:10]:
        print(f"  - {hoja}")

    for hoja in archivo_excel.sheet_names[:5]:
        print()
        print(f"Hoja: {hoja}")

        encontrado = False

        for encabezado in range(0, 15):
            try:
                df = pd.read_excel(
                    ruta,
                    sheet_name=hoja,
                    header=encabezado,
                    nrows=3,
                )

                columnas = [
                    str(columna).strip()
                    for columna in df.columns
                ]

                texto_columnas = " ".join(columnas).lower()

                palabras_columnas = [
                    "provincia",
                    "grado",
                    "curso",
                    "bachiller",
                    "nivel",
                    "estudiante",
                    "matricula",
                    "año",
                    "anio",
                ]

                if any(
                    palabra in texto_columnas
                    for palabra in palabras_columnas
                ):
                    print(f"Encabezado probable en fila: {encabezado + 1}")
                    print("Columnas:")

                    for columna in columnas:
                        print(f"  - {columna}")

                    encontrado = True
                    break

            except Exception:
                continue

        if not encontrado:
            print("No se identificó automáticamente el encabezado.")


def main():
    print("=" * 90)
    print("BÚSQUEDA DE FUENTES MINEDUC")
    print("=" * 90)
    print(f"Proyecto: {BASE_DIR}")

    archivos = [
        ruta
        for ruta in BASE_DIR.rglob("*")
        if ruta.is_file() and es_archivo_relevante(ruta)
    ]

    if not archivos:
        print()
        print("No se encontraron archivos relacionados con MINEDUC o AMIE.")
        return

    print()
    print(f"Archivos encontrados: {len(archivos)}")

    for numero, ruta in enumerate(archivos, start=1):
        print()
        print("=" * 90)
        print(f"ARCHIVO {numero}: {ruta}")
        print(f"Tamaño: {ruta.stat().st_size / (1024 * 1024):.2f} MB")
        print("=" * 90)

        extension = ruta.suffix.lower()

        if extension == ".csv":
            inspeccionar_csv(ruta)

        elif extension in {".xlsx", ".xls"}:
            inspeccionar_excel(ruta)


if __name__ == "__main__":
    main()