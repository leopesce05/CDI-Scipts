import psycopg
import json
from datetime import datetime
import uuid
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

class DBOperations:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.conn = psycopg.connect(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                dbname=os.getenv('DB_NAME')
            )
            self.conn.autocommit = True
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()

    def crear_ejecucion(self, metodo):
        """
        Crea una nueva ejecución en la base de datos
        
        Args:
            metodo (str): ID del método aplicado
        
        Returns:
            str: ID de la ejecución creada
        """
        try:
            execution_id = str(uuid.uuid4())
            with self.conn.cursor() as cursor:
                # Crear ejecución
                cursor.execute(
                    "INSERT INTO ResultadoEjecucion (executionId, metodo_aplicado_id) VALUES (%s, %s)",
                    (execution_id, metodo)
                )
                
                return execution_id
                
        except Exception as e:
            print(f"Error al crear ejecución: {e}")
            raise

    def guardar_resultado_celda(self, execution_id, nombre_tabla, nombre_atributo, id_tupla, valor):
        """
        Guarda el resultado de una celda específica
        
        Args:
            execution_id (str): ID de la ejecución
            nombre_tabla (str): Nombre de la tabla
            nombre_atributo (str): Nombre del atributo
            id_tupla (str): ID de la tupla
            valor (dict): Valor a guardar en formato JSON
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO resultadoCeldaFila 
                    (executionId, nombreTabla, nombreAtributo, idTupla, valorCD)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (execution_id, nombre_tabla, nombre_atributo, id_tupla, json.dumps(valor))
                )
        except Exception as e:
            print(f"Error al guardar resultado de celda: {e}")
            raise

    def guardar_resultado_columna(self, execution_id, nombre_tabla, nombre_atributo, valor):
        """
        Guarda el resultado de una columna completa
        
        Args:
            execution_id (str): ID de la ejecución
            nombre_tabla (str): Nombre de la tabla
            nombre_atributo (str): Nombre del atributo
            valor (dict): Valor a guardar en formato JSON
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO resultadoColumna 
                    (executionId, nombreTabla, nombreAtributo, valorCD)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (execution_id, nombre_tabla, nombre_atributo, json.dumps(valor))
                )
        except Exception as e:
            print(f"Error al guardar resultado de columna: {e}")
            raise

    def obtener_resultados_ejecucion(self, execution_id):
        """
        Obtiene todos los resultados de una ejecución específica
        
        Args:
            execution_id (str): ID de la ejecución
        
        Returns:
            dict: Diccionario con los resultados de la ejecución
        """
        try:
            resultados = {
                'celdas': [],
                'columnas': []
            }
            
            with self.conn.cursor() as cursor:
                # Obtener resultados de celdas
                cursor.execute(
                    """
                    SELECT nombreTabla, nombreAtributo, idTupla, valorCD
                    FROM resultadoCeldaFila
                    WHERE executionId = %s
                    """,
                    (execution_id,)
                )
                for row in cursor.fetchall():
                    resultados['celdas'].append({
                        'tabla': row[0],
                        'atributo': row[1],
                        'tupla': row[2],
                        'valor': json.loads(row[3])
                    })
                
                # Obtener resultados de columnas
                cursor.execute(
                    """
                    SELECT nombreTabla, nombreAtributo, valorCD
                    FROM resultadoColumna
                    WHERE executionId = %s
                    """,
                    (execution_id,)
                )
                for row in cursor.fetchall():
                    resultados['columnas'].append({
                        'tabla': row[0],
                        'atributo': row[1],
                        'valor': json.loads(row[2])
                    })
                
                return resultados
                
        except Exception as e:
            print(f"Error al obtener resultados: {e}")
            raise

# Ejemplo de uso
if __name__ == "__main__":
    try:
        db = DBOperations()
        
        # Crear una nueva ejecución
        execution_id = db.crear_ejecucion(
            metodo="DISTANCE"
        )
        
        # Guardar resultados de celdas
        db.guardar_resultado_celda(
            execution_id=execution_id,
            nombre_tabla="books",
            nombre_atributo="title",
            id_tupla="1",
            valor={"distancia": 0.5, "similar_a": "2"}
        )
        
        # Guardar resultados de columna
        db.guardar_resultado_columna(
            execution_id=execution_id,
            nombre_tabla="books",
            nombre_atributo="title",
            valor={"total_similares": 10, "promedio_distancia": 0.3}
        )
        
        # Obtener resultados
        resultados = db.obtener_resultados_ejecucion(execution_id)
        print("Resultados:", json.dumps(resultados, indent=2))
        
    except Exception as e:
        print(f"Error en ejemplo: {e}")
    finally:
        if 'db' in locals():
            db.close() 