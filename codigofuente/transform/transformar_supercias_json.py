import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "macroentorno.db"
TAMANO_LOTE = 5000


def decodificar_json(texto):
    datos = texto

    for _ in range(5):
        if not isinstance(datos, str):
            break

        try:
            datos = json.loads(datos)
        except (json.JSONDecodeError, TypeError):
            return None

    return datos if isinstance(datos, dict) else None


def crear_tablas(conexion):
    conexion.execute("DROP TABLE IF EXISTS fact_empresas_rpa")

    conexion.execute("""
        CREATE TABLE fact_empresas_rpa (
            periodo_reporte TEXT,
            expediente TEXT,
            ruc TEXT,
            nombre TEXT,
            situacion_legal TEXT,
            fecha_constitucion TEXT,
            tipo_compania TEXT,
            pais TEXT,
            region TEXT,
            provincia TEXT,
            canton TEXT,
            ciudad TEXT,
            calle TEXT,
            numero TEXT,
            barrio TEXT,
            telefono TEXT,
            representante TEXT,
            cargo TEXT,
            capital_suscrito REAL,
            ciiu_n1 TEXT,
            ciiu_n6 TEXT,
            ultimo_balance_anio INTEGER,
            fuente TEXT,
            PRIMARY KEY (periodo_reporte, ruc)
        )
    """)

    conexion.execute("DROP TABLE IF EXISTS fact_ranking_empresas_rpa")

    conexion.execute("""
        CREATE TABLE fact_ranking_empresas_rpa (
            anio INTEGER,
            expediente TEXT,
            ciiu_n1 TEXT,
            ciiu_n6 TEXT,
            posicion_general INTEGER,
            numero_empleados INTEGER,
            ingresos_ventas REAL,
            ingresos_totales REAL,
            utilidad_ejercicio REAL,
            utilidad_neta REAL,
            activos REAL,
            patrimonio REAL,
            gastos_financieros REAL,
            gastos_admin_ventas REAL,
            impuesto_renta REAL,
            roe REAL,
            roa REAL,
            liquidez_corriente REAL,
            margen_operacional REAL,
            margen_bruto REAL,
            endeudamiento_activo REAL,
            endeudamiento_patrimonial REAL,
            PRIMARY KEY (anio, expediente)
        )
    """)

    conexion.commit()


def transformar_directorio(conexion):
    print()
    print("=" * 70)
    print("TRANSFORMANDO SUPERCIAS_DIRECTORIO")
    print("=" * 70)

    cursor = conexion.execute("""
        SELECT datos_json
        FROM raw_supercias_consolidado
        WHERE indicador = 'SUPERCIAS_DIRECTORIO'
          AND datos_json IS NOT NULL
    """)

    lote = []
    procesados = 0
    errores = 0

    while True:
        filas = cursor.fetchmany(TAMANO_LOTE)

        if not filas:
            break

        for (texto_json,) in filas:
            datos = decodificar_json(texto_json)

            if datos is None:
                errores += 1
                continue

            empresa = datos.get("empresa_metadata", {})
            ubicacion = datos.get("ubicacion", {})
            financiero = datos.get("financiero_ciiu", {})

            registro = (
                datos.get("periodo_reporte"),
                str(empresa.get("expediente", "")),
                str(empresa.get("ruc", "")),
                empresa.get("nombre"),
                empresa.get("situacion_legal"),
                empresa.get("fecha_constitucion"),
                empresa.get("tipo_compania"),
                ubicacion.get("pais"),
                ubicacion.get("region"),
                ubicacion.get("provincia"),
                ubicacion.get("canton"),
                ubicacion.get("ciudad"),
                ubicacion.get("calle"),
                ubicacion.get("numero"),
                ubicacion.get("barrio"),
                ubicacion.get("telefono"),
                financiero.get("representante"),
                financiero.get("cargo"),
                financiero.get("capital_suscrito"),
                financiero.get("ciiu_nivel1"),
                financiero.get("ciiu_nivel6"),
                financiero.get("ultimo_balance_anio"),
                datos.get("fuente"),
            )

            lote.append(registro)
            procesados += 1

        conexion.executemany("""
            INSERT OR REPLACE INTO fact_empresas_rpa (
                periodo_reporte,
                expediente,
                ruc,
                nombre,
                situacion_legal,
                fecha_constitucion,
                tipo_compania,
                pais,
                region,
                provincia,
                canton,
                ciudad,
                calle,
                numero,
                barrio,
                telefono,
                representante,
                cargo,
                capital_suscrito,
                ciiu_n1,
                ciiu_n6,
                ultimo_balance_anio,
                fuente
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, lote)

        conexion.commit()
        lote.clear()

        if procesados % 50000 < TAMANO_LOTE:
            print(f"Directorio procesado: {procesados:,}")

    print(f"Registros procesados: {procesados:,}")
    print(f"Errores JSON: {errores:,}")


def transformar_ranking(conexion):
    print()
    print("=" * 70)
    print("TRANSFORMANDO SUPERCIAS_RANKING")
    print("=" * 70)

    cursor = conexion.execute("""
        SELECT datos_json
        FROM raw_supercias_consolidado
        WHERE indicador = 'SUPERCIAS_RANKING'
          AND datos_json IS NOT NULL
    """)

    lote = []
    procesados = 0
    errores = 0

    while True:
        filas = cursor.fetchmany(TAMANO_LOTE)

        if not filas:
            break

        for (texto_json,) in filas:
            datos = decodificar_json(texto_json)

            if datos is None:
                errores += 1
                continue

            registro = (
                datos.get("ANIO"),
                str(datos.get("EXPEDIENTE", "")),
                datos.get("CIIU_N1"),
                datos.get("CIIU_N6"),
                datos.get("POSICION_GENERAL"),
                datos.get("N_EMPLEADOS"),
                datos.get("INGRESOS_VENTAS"),
                datos.get("INGRESOS_TOTALES"),
                datos.get("UTILIDAD_EJERCICIO"),
                datos.get("UTILIDAD_NETA"),
                datos.get("ACTIVOS"),
                datos.get("PATRIMONIO"),
                datos.get("GASTOS_FINANCIEROS"),
                datos.get("GASTOS_ADMIN_VENTAS"),
                datos.get("IMPUESTO_RENTA"),
                datos.get("ROE"),
                datos.get("ROA"),
                datos.get("LIQUIDEZ_CORRIENTE"),
                datos.get("MARGEN_OPERACIONAL"),
                datos.get("MARGEN_BRUTO"),
                datos.get("END_ACTIVO"),
                datos.get("END_PATRIMONIAL"),
            )

            lote.append(registro)
            procesados += 1

        conexion.executemany("""
            INSERT OR REPLACE INTO fact_ranking_empresas_rpa (
                anio,
                expediente,
                ciiu_n1,
                ciiu_n6,
                posicion_general,
                numero_empleados,
                ingresos_ventas,
                ingresos_totales,
                utilidad_ejercicio,
                utilidad_neta,
                activos,
                patrimonio,
                gastos_financieros,
                gastos_admin_ventas,
                impuesto_renta,
                roe,
                roa,
                liquidez_corriente,
                margen_operacional,
                margen_bruto,
                endeudamiento_activo,
                endeudamiento_patrimonial
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, lote)

        conexion.commit()
        lote.clear()

        if procesados % 100000 < TAMANO_LOTE:
            print(f"Ranking procesado: {procesados:,}")

    print(f"Registros procesados: {procesados:,}")
    print(f"Errores JSON: {errores:,}")


def crear_vista_integrada(conexion):
    conexion.execute("DROP VIEW IF EXISTS vw_empresas_ranking_rpa")

    conexion.execute("""
        CREATE VIEW vw_empresas_ranking_rpa AS
        SELECT
            r.anio,
            r.expediente,
            d.ruc,
            d.nombre,
            d.situacion_legal,
            d.tipo_compania,
            d.region,
            d.provincia,
            d.canton,
            COALESCE(r.ciiu_n1, d.ciiu_n1) AS ciiu_n1,
            COALESCE(r.ciiu_n6, d.ciiu_n6) AS ciiu_n6,
            d.capital_suscrito,
            r.posicion_general,
            r.numero_empleados,
            r.ingresos_ventas,
            r.ingresos_totales,
            r.utilidad_ejercicio,
            r.utilidad_neta,
            r.activos,
            r.patrimonio,
            r.roe,
            r.roa,
            r.liquidez_corriente,
            r.margen_operacional,
            r.endeudamiento_activo
        FROM fact_ranking_empresas_rpa r
        LEFT JOIN fact_empresas_rpa d
            ON r.expediente = d.expediente
    """)

    conexion.commit()


def mostrar_resumen(conexion):
    directorio = conexion.execute(
        "SELECT COUNT(*) FROM fact_empresas_rpa"
    ).fetchone()[0]

    ranking = conexion.execute(
        "SELECT COUNT(*) FROM fact_ranking_empresas_rpa"
    ).fetchone()[0]

    integrados = conexion.execute(
        "SELECT COUNT(*) FROM vw_empresas_ranking_rpa"
    ).fetchone()[0]

    con_provincia = conexion.execute("""
        SELECT COUNT(*)
        FROM vw_empresas_ranking_rpa
        WHERE provincia IS NOT NULL
          AND TRIM(provincia) <> ''
    """).fetchone()[0]

    print()
    print("=" * 70)
    print("RESUMEN DE TRANSFORMACIÓN")
    print("=" * 70)
    print(f"Empresas en directorio: {directorio:,}")
    print(f"Registros financieros: {ranking:,}")
    print(f"Registros integrados: {integrados:,}")
    print(f"Registros con provincia: {con_provincia:,}")


def main():
    print(f"Base de datos: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conexion:
        crear_tablas(conexion)
        transformar_directorio(conexion)
        transformar_ranking(conexion)
        crear_vista_integrada(conexion)
        mostrar_resumen(conexion)

    print()
    print("Transformación SUPERCIAS terminada correctamente.")


if __name__ == "__main__":
    main()