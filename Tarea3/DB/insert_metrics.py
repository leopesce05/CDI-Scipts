import psycopg
from db_operations import DBOperations

def insert_metrics():
    try:
        # Estructura de datos con métricas y sus factores asociados
        metrics_factors = {
            "ExactSint-ReglaCorrecta": "Exactitud Sintáctica",
            "ExactSint-Desviacion": "Exactitud Sintáctica",
            "Densidad-Grado": "Densidad",
            "NoDuplicación-CantDups": "No Duplicación",
            "IntDominio-OutBounds-Gen": "Integridad de Dominio",
            "IntDominio-OutBounds-Esp": "Integridad de Dominio",
            "Precisión-CifrasSign-Bool": "Precisión",
            "IntInterRel-Pertenece": "Integridad Interrelación"
        }

        # Conectar a la base de datos
        db = DBOperations()
        
        print("Iniciando inserción de métricas...")
        
        # Insertar cada métrica
        for metric_id, factor_nombre in metrics_factors.items():
            print(f"\nInsertando métrica: {metric_id}")
            try:
                # Insertar métrica
                with db.conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Metrica (id_metrica, factor_nombre) VALUES (%s, %s)",
                        (metric_id, factor_nombre)
                    )
                print(f"✓ Métrica '{metric_id}' insertada correctamente para el factor '{factor_nombre}'")
                
            except Exception as e:
                print(f"✗ Error al insertar métrica '{metric_id}': {e}")

        print("\n¡Proceso completado!")
        
    except Exception as e:
        print(f"Error durante la inserción: {e}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    insert_metrics() 