import psycopg
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

def crear_base_datos():
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
                PRIMARY KEY (executionId, nombreTabla, nombreAtributo),
                FOREIGN KEY (executionId) REFERENCES ResultadoEjecucion(executionId) ON DELETE CASCADE
            )
            ''')
            
            conn.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    crear_base_datos()