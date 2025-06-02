import psycopg
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def crear_base_datos():
    """Crea la base de datos y sus tablas"""
    try:
        # Primero conectamos a postgres para crear la base de datos
        conn = psycopg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname="postgres"
        )
        
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'db_cdi'")
            if not cursor.fetchone():
                cursor.execute('CREATE DATABASE db_cdi')
        
        conn.close()

        # Ahora conectamos a nuestra base de datos para crear las tablas
        conn = psycopg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME')
        )
        
        with conn.cursor() as cursor:
            # Crear tablas
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Dimension (
                Nombre VARCHAR(100) PRIMARY KEY
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Factor (
                Nombre VARCHAR(100) PRIMARY KEY,
                dimension_nombre VARCHAR(100) NOT NULL,
                FOREIGN KEY (dimension_nombre) REFERENCES Dimension(Nombre)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Metrica (
                id_metrica VARCHAR(50) PRIMARY KEY,
                factor_nombre VARCHAR(100) NOT NULL,
                FOREIGN KEY (factor_nombre) REFERENCES Factor(Nombre)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Metodo (
                id_metodo VARCHAR(50) PRIMARY KEY,
                metrica_id VARCHAR(50) NOT NULL,
                FOREIGN KEY (metrica_id) REFERENCES Metrica(id_metrica)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS MetodoAplicado (
                id_metodo_aplicado VARCHAR(50) PRIMARY KEY,
                metodo_id VARCHAR(50) NOT NULL,
                FOREIGN KEY (metodo_id) REFERENCES Metodo(id_metodo)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ResultadoEjecucion (
                executionId VARCHAR(50) PRIMARY KEY,
                metodo_aplicado_id VARCHAR(50) NOT NULL,
                fecha TIMESTAMPTZ DEFAULT NOW(),
                FOREIGN KEY (metodo_aplicado_id) REFERENCES MetodoAplicado(id_metodo_aplicado)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultadoCeldaFila (
                executionId VARCHAR(50) NOT NULL,
                nombreTabla VARCHAR(100) NOT NULL,
                nombreAtributo VARCHAR(100) NOT NULL,
                idTupla VARCHAR(50) NOT NULL,
                valorCD JSONB NOT NULL,
                calidad VARCHAR(20) NOT NULL,
                PRIMARY KEY (executionId, nombreTabla, nombreAtributo, idTupla),
                FOREIGN KEY (executionId) REFERENCES ResultadoEjecucion(executionId) ON DELETE CASCADE
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultadoColumna (
                executionId VARCHAR(50) NOT NULL,
                nombreTabla VARCHAR(100) NOT NULL,
                nombreAtributo VARCHAR(100) NOT NULL,
                valorCD JSONB NOT NULL,
                calidad VARCHAR(20) NOT NULL,
                PRIMARY KEY (executionId, nombreTabla, nombreAtributo),
                FOREIGN KEY (executionId) REFERENCES ResultadoEjecucion(executionId) ON DELETE CASCADE
            )
            ''')
            
            conn.commit()
            print("✓ Base de datos y tablas creadas correctamente")

    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def insert_dimensions_and_factors():
    """Inserta las dimensiones y factores en la base de datos"""
    try:
        conn = psycopg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME')
        )
        
        # Estructura de datos con dimensiones y sus factores
        dimensions_factors = {
            "Exactitud": [
                "Exactitud Sintactica",
                "Precision"
            ],
            "Completitud": [
                "Densidad"
            ],
            "Consistencia": [
                "Integridad de Dominio",
                "Integridad Interrelacion"
            ],
            "Unicidad": [
                "No Duplicacion"
            ]
        }

        with conn.cursor() as cursor:
            # Insertar cada dimensión y sus factores
            for dimension, factors in dimensions_factors.items():
                try:
                    cursor.execute(
                        "INSERT INTO Dimension (Nombre) VALUES (%s)",
                        (dimension,)
                    )
                    print(f"✓ Dimensión '{dimension}' insertada correctamente")
                except Exception as e:
                    print(f"  - La dimensión '{dimension}' ya existe o hubo un error: {e}")
                
                # Para cada factor en la dimensión
                for factor in factors:
                    try:
                        cursor.execute(
                            "INSERT INTO Factor (Nombre, dimension_nombre) VALUES (%s, %s)",
                            (factor, dimension)
                        )
                        print(f"  ✓ Factor '{factor}' insertado correctamente")
                    except Exception as e:
                        print(f"  ✗ Error al insertar factor '{factor}': {e}")

        conn.commit()
        print("\n✓ Dimensiones y factores insertados correctamente")

    except Exception as e:
        print(f"Error al insertar dimensiones y factores: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def insert_metrics():
    """Inserta las métricas en la base de datos"""
    try:
        conn = psycopg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME')
        )
        
        # Estructura de datos con métricas y sus factores asociados
        metrics_factors = {
            "ExactSint-ReglaCorrecta": "Exactitud Sintactica",
            "ExactSint-Desviacion": "Exactitud Sintactica",
            "Densidad-Grado": "Densidad",
            "NoDuplicacion-CantDups": "No Duplicacion",
            "IntDominio-OutBounds-Gen": "Integridad de Dominio",
            "IntDominio-OutBounds-Esp": "Integridad de Dominio",
            "Precision-Granularidad": "Precision",
            "IntInterRel-Pertenece": "Integridad Interrelacion"
        }

        with conn.cursor() as cursor:
            # Insertar cada métrica
            for metric_id, factor_nombre in metrics_factors.items():
                try:
                    cursor.execute(
                        "INSERT INTO Metrica (id_metrica, factor_nombre) VALUES (%s, %s)",
                        (metric_id, factor_nombre)
                    )
                    print(f"✓ Métrica '{metric_id}' insertada correctamente para el factor '{factor_nombre}'")
                except Exception as e:
                    print(f"✗ Error al insertar métrica '{metric_id}': {e}")

        conn.commit()
        print("\n✓ Métricas insertadas correctamente")

    except Exception as e:
        print(f"Error al insertar métricas: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def insert_methods():
    """Inserta los métodos y métodos aplicados en la base de datos"""
    try:
        conn = psycopg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME')
        )
        
        # Estructura de datos con métodos, sus aplicados y la métrica asociada
        methods_data = [
            {
                "metodo_id": "ExactSint-ReglaCorrecta-ISBN",
                "metodo_aplicado_id": "ExactSint-ReglaCorrecta-ISBN_ap",
                "metrica_id": "ExactSint-ReglaCorrecta"
            },
            {
                "metodo_id": "ExactSint-LeveshteinDistanceInterCSV",
                "metodo_aplicado_id": "ExactSint-LeveshteinDistanceInterCSV_ap",
                "metrica_id": "ExactSint-Desviacion"
            },
            {
                "metodo_id": "Densidad-Grado-Contar",
                "metodo_aplicado_id": "Densidad-Grado-Contar_ap",
                "metrica_id": "Densidad-Grado"
            },
            {
                "metodo_id": "NoDuplicacion-CantDups-Contar",
                "metodo_aplicado_id": "NoDuplicacion-CantDups-Contar_ap",
                "metrica_id": "NoDuplicacion-CantDups"
            },
            {
                "metodo_id": "IntDominio-OutBounds-Gen-ContarNum",
                "metodo_aplicado_id": "IntDominio-OutBounds-Gen-ContarNum_ap",
                "metrica_id": "IntDominio-OutBounds-Gen"
            },
            {
                "metodo_id": "IntDominio-OutBounds-Esp-ContarNum",
                "metodo_aplicado_id": "IntDominio-OutBounds-Esp-ContarNum_ap",
                "metrica_id": "IntDominio-OutBounds-Esp"
            },
            {
                "metodo_id": "IntInterRel-Pertenencia",
                "metodo_aplicado_id": "IntInterRel-Pertenencia_ap",
                "metrica_id": "IntInterRel-Pertenece"
            },
            {
                "metodo_id": "Precision-Fechas",
                "metodo_aplicado_id": "Precision-Fechas_ap",
                "metrica_id": "Precision-Granularidad"
            }
        ]

        with conn.cursor() as cursor:
            # Insertar cada método y su método aplicado
            for method in methods_data:
                try:
                    # Insertar método
                    cursor.execute(
                        "INSERT INTO Metodo (id_metodo, metrica_id) VALUES (%s, %s)",
                        (method['metodo_id'], method['metrica_id'])
                    )
                    print(f"✓ Método '{method['metodo_id']}' insertado correctamente")
                    
                    # Insertar método aplicado
                    cursor.execute(
                        "INSERT INTO MetodoAplicado (id_metodo_aplicado, metodo_id) VALUES (%s, %s)",
                        (method['metodo_aplicado_id'], method['metodo_id'])
                    )
                    print(f"✓ Método aplicado '{method['metodo_aplicado_id']}' insertado correctamente")
                    
                except Exception as e:
                    print(f"✗ Error al insertar método '{method['metodo_id']}': {e}")

        conn.commit()
        print("\n✓ Métodos y métodos aplicados insertados correctamente")

    except Exception as e:
        print(f"Error al insertar métodos: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def init_database():
    """Inicializa la base de datos con todas las tablas y datos necesarios"""
    try:
        crear_base_datos()
        insert_dimensions_and_factors()
        insert_metrics()
        insert_methods()
        print("\n✓ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise

if __name__ == "__main__":
    init_database() 