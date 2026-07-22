import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "macroentorno.db"


def crear_gold_empresas_provincia(conexion):
    conexion.execute("DROP TABLE IF EXISTS gold_empresas_provincia")

    conexion.execute("""
        CREATE TABLE gold_empresas_provincia AS
        SELECT
            periodo_reporte,
            COALESCE(NULLIF(TRIM(provincia), ''), 'SIN INFORMACIÓN') AS provincia,
            COUNT(DISTINCT ruc) AS total_empresas,
            SUM(COALESCE(capital_suscrito, 0)) AS capital_suscrito_total
        FROM fact_empresas_rpa
        GROUP BY
            periodo_reporte,
            COALESCE(NULLIF(TRIM(provincia), ''), 'SIN INFORMACIÓN')
    """)

    conexion.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_gold_empresas_provincia
        ON gold_empresas_provincia(periodo_reporte, provincia)
    """)


def crear_gold_empresas_situacion(conexion):
    conexion.execute("DROP TABLE IF EXISTS gold_empresas_situacion")

    conexion.execute("""
        CREATE TABLE gold_empresas_situacion AS
        SELECT
            periodo_reporte,
            COALESCE(
                NULLIF(TRIM(situacion_legal), ''),
                'SIN INFORMACIÓN'
            ) AS situacion_legal,
            COUNT(DISTINCT ruc) AS total_empresas
        FROM fact_empresas_rpa
        GROUP BY
            periodo_reporte,
            COALESCE(
                NULLIF(TRIM(situacion_legal), ''),
                'SIN INFORMACIÓN'
            )
    """)


def crear_gold_empresas_ciiu(conexion):
    conexion.execute("DROP TABLE IF EXISTS gold_empresas_ciiu")

    conexion.execute("""
        CREATE TABLE gold_empresas_ciiu AS
        SELECT
            periodo_reporte,
            COALESCE(NULLIF(TRIM(ciiu_n1), ''), 'SIN CIIU') AS ciiu_n1,
            COUNT(DISTINCT ruc) AS total_empresas,
            SUM(COALESCE(capital_suscrito, 0)) AS capital_suscrito_total
        FROM fact_empresas_rpa
        GROUP BY
            periodo_reporte,
            COALESCE(NULLIF(TRIM(ciiu_n1), ''), 'SIN CIIU')
    """)


def crear_gold_ranking_provincia_anio(conexion):
    conexion.execute("DROP TABLE IF EXISTS gold_ranking_provincia_anio")

    conexion.execute("""
        CREATE TABLE gold_ranking_provincia_anio AS
        SELECT
            anio,
            COALESCE(NULLIF(TRIM(provincia), ''), 'SIN INFORMACIÓN') AS provincia,
            COUNT(DISTINCT expediente) AS total_empresas,
            SUM(COALESCE(numero_empleados, 0)) AS total_empleados,
            SUM(COALESCE(ingresos_ventas, 0)) AS ingresos_ventas_total,
            SUM(COALESCE(ingresos_totales, 0)) AS ingresos_totales,
            SUM(COALESCE(utilidad_neta, 0)) AS utilidad_neta_total,
            SUM(COALESCE(activos, 0)) AS activos_total,
            SUM(COALESCE(patrimonio, 0)) AS patrimonio_total,
            AVG(roe) AS roe_promedio,
            AVG(roa) AS roa_promedio,
            AVG(liquidez_corriente) AS liquidez_promedio
        FROM vw_empresas_ranking_rpa
        GROUP BY
            anio,
            COALESCE(NULLIF(TRIM(provincia), ''), 'SIN INFORMACIÓN')
    """)

    conexion.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_gold_ranking_provincia_anio
        ON gold_ranking_provincia_anio(anio, provincia)
    """)


def crear_gold_ranking_ciiu_anio(conexion):
    conexion.execute("DROP TABLE IF EXISTS gold_ranking_ciiu_anio")

    conexion.execute("""
        CREATE TABLE gold_ranking_ciiu_anio AS
        SELECT
            anio,
            COALESCE(NULLIF(TRIM(ciiu_n1), ''), 'SIN CIIU') AS ciiu_n1,
            COUNT(DISTINCT expediente) AS total_empresas,
            SUM(COALESCE(numero_empleados, 0)) AS total_empleados,
            SUM(COALESCE(ingresos_ventas, 0)) AS ingresos_ventas_total,
            SUM(COALESCE(utilidad_neta, 0)) AS utilidad_neta_total,
            SUM(COALESCE(activos, 0)) AS activos_total,
            SUM(COALESCE(patrimonio, 0)) AS patrimonio_total
        FROM vw_empresas_ranking_rpa
        GROUP BY
            anio,
            COALESCE(NULLIF(TRIM(ciiu_n1), ''), 'SIN CIIU')
    """)


def crear_gold_resumen_supercias(conexion):
    conexion.execute("DROP TABLE IF EXISTS gold_resumen_supercias")

    conexion.execute("""
        CREATE TABLE gold_resumen_supercias AS
        SELECT
            anio,
            COUNT(DISTINCT expediente) AS total_empresas,
            SUM(COALESCE(numero_empleados, 0)) AS total_empleados,
            SUM(COALESCE(ingresos_ventas, 0)) AS ingresos_ventas_total,
            SUM(COALESCE(ingresos_totales, 0)) AS ingresos_totales,
            SUM(COALESCE(utilidad_neta, 0)) AS utilidad_neta_total,
            SUM(COALESCE(activos, 0)) AS activos_total,
            SUM(COALESCE(patrimonio, 0)) AS patrimonio_total
        FROM vw_empresas_ranking_rpa
        GROUP BY anio
        ORDER BY anio
    """)


def mostrar_resumen(conexion):
    tablas = [
        "gold_empresas_provincia",
        "gold_empresas_situacion",
        "gold_empresas_ciiu",
        "gold_ranking_provincia_anio",
        "gold_ranking_ciiu_anio",
        "gold_resumen_supercias",
    ]

    print()
    print("=" * 75)
    print("RESUMEN DE TABLAS GOLD")
    print("=" * 75)

    for tabla in tablas:
        total = conexion.execute(
            f"SELECT COUNT(*) FROM {tabla}"
        ).fetchone()[0]

        print(f"{tabla}: {total:,} filas")


def mostrar_top_provincias(conexion):
    print()
    print("=" * 75)
    print("TOP 10 PROVINCIAS POR NÚMERO DE EMPRESAS")
    print("=" * 75)

    filas = conexion.execute("""
        SELECT
            provincia,
            SUM(total_empresas) AS total
        FROM gold_empresas_provincia
        WHERE provincia <> 'SIN INFORMACIÓN'
        GROUP BY provincia
        ORDER BY total DESC
        LIMIT 10
    """).fetchall()

    for provincia, total in filas:
        print(f"{provincia}: {total:,}")


def main():
    if not DB_PATH.exists():
        print(f"ERROR: no existe la base de datos: {DB_PATH}")
        raise SystemExit(1)

    print("=" * 75)
    print("CREACIÓN DE TABLAS GOLD DE SUPERCIAS")
    print("=" * 75)
    print(f"Base de datos: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conexion:
        crear_gold_empresas_provincia(conexion)
        crear_gold_empresas_situacion(conexion)
        crear_gold_empresas_ciiu(conexion)
        crear_gold_ranking_provincia_anio(conexion)
        crear_gold_ranking_ciiu_anio(conexion)
        crear_gold_resumen_supercias(conexion)

        conexion.commit()

        mostrar_resumen(conexion)
        mostrar_top_provincias(conexion)

    print()
    print("Tablas Gold de SUPERCIAS creadas correctamente.")


if __name__ == "__main__":
    main()