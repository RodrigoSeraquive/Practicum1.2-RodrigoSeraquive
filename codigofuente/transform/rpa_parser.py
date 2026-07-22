import re
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVOS_SQL = [
    BASE_DIR / "data_raw" / "supercias" / "sql" / "tab_consolidado_export.sql",
    BASE_DIR / "data_raw" / "supercias" / "sql" / "tab_consolidado_supercias.sql",
]

DB_PATH = BASE_DIR / "db" / "macroentorno.db"

TAMANO_LOTE = 5000


def dividir_valores_sql(texto):
    """
    Divide los valores de un INSERT respetando:
    - textos entre comillas simples;
    - funciones como TO_DATE(...);
    - JSON con comas.
    """
    valores = []
    actual = []
    dentro_comillas = False
    nivel_parentesis = 0
    i = 0

    while i < len(texto):
        caracter = texto[i]

        if caracter == "'":
            actual.append(caracter)

            if dentro_comillas:
                if i + 1 < len(texto) and texto[i + 1] == "'":
                    actual.append("'")
                    i += 1
                else:
                    dentro_comillas = False
            else:
                dentro_comillas = True

        elif not dentro_comillas:
            if caracter == "(":
                nivel_parentesis += 1
                actual.append(caracter)

            elif caracter == ")":
                nivel_parentesis -= 1
                actual.append(caracter)

            elif caracter == "," and nivel_parentesis == 0:
                valores.append("".join(actual).strip())
                actual = []

            else:
                actual.append(caracter)

        else:
            actual.append(caracter)

        i += 1

    if actual:
        valores.append("".join(actual).strip())

    return valores


def limpiar_texto_sql(valor):
    valor = valor.strip()

    if valor.upper() == "NULL":
        return None

    if valor.startswith("'") and valor.endswith("'"):
        valor = valor[1:-1]
        valor = valor.replace("''", "'")

    return valor


def obtener_fecha(valor):
    if not valor:
        return None

    coincidencia = re.search(
        r"TO_DATE\('([^']+)'",
        valor,
        flags=re.IGNORECASE
    )

    if coincidencia:
        return coincidencia.group(1)

    return limpiar_texto_sql(valor)


def procesar_linea(linea):
    texto_mayuscula = linea.upper()

    if "INSERT INTO TAB_CONSOLIDADO" not in texto_mayuscula:
        return None

    posicion = texto_mayuscula.find("VALUES")

    if posicion == -1:
        return None

    parte_valores = linea[posicion + len("VALUES"):].strip()

    if parte_valores.startswith("("):
        parte_valores = parte_valores[1:]

    if parte_valores.endswith(";"):
        parte_valores = parte_valores[:-1].strip()

    if parte_valores.endswith(")"):
        parte_valores = parte_valores[:-1]

    valores = dividir_valores_sql(parte_valores)

    if len(valores) < 9:
        return None

    identificador = limpiar_texto_sql(valores[0])
    indicador = limpiar_texto_sql(valores[1])
    fecha_extraccion = obtener_fecha(valores[2])
    estado = limpiar_texto_sql(valores[3])
    necesita_respaldo = limpiar_texto_sql(valores[4])
    detalle_error = limpiar_texto_sql(valores[5])
    datos_json = limpiar_texto_sql(valores[6])
    dato_clave = limpiar_texto_sql(valores[7])
    hash_contenido = limpiar_texto_sql(valores[8])

    return (
        identificador,
        indicador,
        fecha_extraccion,
        estado,
        necesita_respaldo,
        detalle_error,
        datos_json,
        dato_clave,
        hash_contenido,
    )


def crear_tabla(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS raw_supercias_consolidado (
            id_original TEXT,
            indicador TEXT NOT NULL,
            fecha_extraccion TEXT,
            estado TEXT,
            necesita_respaldo TEXT,
            detalle_error TEXT,
            datos_json TEXT,
            dato_clave TEXT NOT NULL,
            hash_contenido TEXT,
            archivo_origen TEXT,
            PRIMARY KEY (indicador, dato_clave)
        )
    """)

    conexion.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_raw_supercias_indicador
        ON raw_supercias_consolidado(indicador)
    """)

    conexion.commit()


def guardar_lote(conexion, lote):
    conexion.executemany("""
        INSERT INTO raw_supercias_consolidado (
            id_original,
            indicador,
            fecha_extraccion,
            estado,
            necesita_respaldo,
            detalle_error,
            datos_json,
            dato_clave,
            hash_contenido,
            archivo_origen
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(indicador, dato_clave)
        DO UPDATE SET
            id_original = excluded.id_original,
            fecha_extraccion = excluded.fecha_extraccion,
            estado = excluded.estado,
            necesita_respaldo = excluded.necesita_respaldo,
            detalle_error = excluded.detalle_error,
            datos_json = excluded.datos_json,
            hash_contenido = excluded.hash_contenido,
            archivo_origen = excluded.archivo_origen
    """, lote)

    conexion.commit()


def procesar_archivo(conexion, ruta):
    if not ruta.exists():
        print(f"ERROR: no existe el archivo: {ruta}")
        return

    print()
    print("=" * 70)
    print(f"Procesando: {ruta.name}")
    print("=" * 70)

    lote = []
    procesados = 0
    errores = 0

    with ruta.open(
        mode="r",
        encoding="utf-8",
        errors="replace"
    ) as archivo:

        for numero_linea, linea in enumerate(archivo, start=1):
            try:
                registro = procesar_linea(linea)

                if registro is None:
                    continue

                lote.append(registro + (ruta.name,))
                procesados += 1

                if len(lote) >= TAMANO_LOTE:
                    guardar_lote(conexion, lote)
                    lote.clear()

                if procesados % 100000 == 0:
                    print(f"Registros procesados: {procesados:,}")

            except Exception as error:
                errores += 1

                if errores <= 10:
                    print(
                        f"Error en línea {numero_linea}: "
                        f"{type(error).__name__}: {error}"
                    )

    if lote:
        guardar_lote(conexion, lote)

    print(f"Finalizado: {ruta.name}")
    print(f"Registros leídos: {procesados:,}")
    print(f"Errores encontrados: {errores:,}")


def mostrar_resultados(conexion):
    print()
    print("=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)

    resultados = conexion.execute("""
        SELECT
            indicador,
            COUNT(*) AS total
        FROM raw_supercias_consolidado
        GROUP BY indicador
        ORDER BY indicador
    """).fetchall()

    for indicador, total in resultados:
        print(f"{indicador}: {total:,}")

    total_general = conexion.execute("""
        SELECT COUNT(*)
        FROM raw_supercias_consolidado
    """).fetchone()[0]

    print("-" * 70)
    print(f"Total almacenado en SQLite: {total_general:,}")


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Base de datos: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conexion:
        crear_tabla(conexion)

        for archivo_sql in ARCHIVOS_SQL:
            procesar_archivo(conexion, archivo_sql)

        mostrar_resultados(conexion)

    print()
    print("Proceso terminado correctamente.")


if __name__ == "__main__":
    main()