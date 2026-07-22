from pathlib import Path
import subprocess
import sys
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
TRANSFORM_DIR = BASE_DIR / "transform"


PASOS_PIPELINE = [
    {
        "nombre": "Procesar archivos SQL de RPA",
        "script": TRANSFORM_DIR / "rpa_parser.py",
    },
    {
        "nombre": "Transformar datos de SUPERCIAS",
        "script": TRANSFORM_DIR / "transformar_supercias_json.py",
    },
    {
        "nombre": "Crear tablas Gold de SUPERCIAS",
        "script": TRANSFORM_DIR / "crear_gold_supercias.py",
    },
    {
        "nombre": "Exportar Gold de SUPERCIAS a CSV",
        "script": TRANSFORM_DIR / "exportar_gold_supercias_csv.py",
    },
    {
        "nombre": "Crear Gold de estudiantes y empresas",
        "script": TRANSFORM_DIR / "crear_gold_bachilleres_empresas.py",
    },
]


def imprimir_linea():
    print("=" * 90)


def verificar_script(ruta_script: Path):
    if not ruta_script.exists():
        raise FileNotFoundError(
            f"No se encontró el script:\n{ruta_script}"
        )

    if not ruta_script.is_file():
        raise FileNotFoundError(
            f"La ruta no corresponde a un archivo:\n{ruta_script}"
        )


def ejecutar_script(numero: int, total: int, nombre: str, ruta_script: Path):
    verificar_script(ruta_script)

    imprimir_linea()
    print(f"PASO {numero} DE {total}")
    print(nombre)
    print(f"Script: {ruta_script}")
    imprimir_linea()

    inicio = datetime.now()

    resultado = subprocess.run(
        [
            sys.executable,
            str(ruta_script),
        ],
        cwd=str(BASE_DIR),
        text=True,
    )

    fin = datetime.now()
    duracion = fin - inicio

    if resultado.returncode != 0:
        print()
        imprimir_linea()
        print("ERROR EN EL PIPELINE")
        imprimir_linea()
        print(f"Paso fallido: {nombre}")
        print(f"Script: {ruta_script}")
        print(f"Código de salida: {resultado.returncode}")
        print(f"Duración: {duracion}")

        raise SystemExit(resultado.returncode)

    print()
    print(f"Paso completado correctamente: {nombre}")
    print(f"Duración: {duracion}")
    print()


def ejecutar_pipeline():
    inicio_pipeline = datetime.now()
    total_pasos = len(PASOS_PIPELINE)

    print()
    imprimir_linea()
    print("INICIO DEL PIPELINE DE DATOS DEL MACROENTORNO")
    imprimir_linea()
    print(f"Proyecto: {BASE_DIR}")
    print(f"Python: {sys.executable}")
    print(f"Fecha y hora: {inicio_pipeline.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total de pasos: {total_pasos}")
    print()

    for numero, paso in enumerate(PASOS_PIPELINE, start=1):
        ejecutar_script(
            numero=numero,
            total=total_pasos,
            nombre=paso["nombre"],
            ruta_script=paso["script"],
        )

    fin_pipeline = datetime.now()
    duracion_total = fin_pipeline - inicio_pipeline

    imprimir_linea()
    print("PIPELINE COMPLETADO CORRECTAMENTE")
    imprimir_linea()
    print(f"Fecha y hora final: {fin_pipeline.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duración total: {duracion_total}")
    print()
    print("Resultados principales:")
    print(
        BASE_DIR
        / "gold"
        / "gold_bachilleres_vs_empresas.csv"
    )
    print(
        BASE_DIR
        / "db"
        / "macroentorno.db"
    )
    imprimir_linea()


if __name__ == "__main__":
    try:
        ejecutar_pipeline()

    except KeyboardInterrupt:
        print()
        imprimir_linea()
        print("PIPELINE INTERRUMPIDO POR EL USUARIO")
        imprimir_linea()
        raise SystemExit(130)

    except Exception as error:
        print()
        imprimir_linea()
        print("ERROR GENERAL DEL PIPELINE")
        imprimir_linea()
        print(type(error).__name__)
        print(error)
        raise SystemExit(1)