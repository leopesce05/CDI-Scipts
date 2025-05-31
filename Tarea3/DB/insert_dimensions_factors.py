import psycopg
from db_operations import DBOperations

def insert_dimensions_and_factors():
    try:
        # Estructura de datos con dimensiones y sus factores
        dimensions_factors = {
            "Exactitud": [
                "Exactitud Sintáctica",
                "Precisión"
            ],
            "Completitud": [
                "Densidad"
            ],
            "Consistencia": [
                "Integridad de Dominio",
                "Integridad Interrelación"
            ],
            "Unicidad": [
                "No Duplicación"
            ]
        }

        # Conectar a la base de datos
        db = DBOperations()
        
        # Insertar cada dimensión y sus factores
        for dimension, factors in dimensions_factors.items():
            print(f"\nInsertando dimensión: {dimension}")
            
            try:
                # Insertar dimensión directamente
                with db.conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Dimension (Nombre) VALUES (%s)",
                        (dimension,)
                    )
                print(f"✓ Dimensión '{dimension}' insertada correctamente")
            except Exception as e:
                print(f"  - La dimensión '{dimension}' ya existe o hubo un error: {e}")
            
            # Para cada factor en la dimensión
            for factor in factors:
                print(f"\n  Insertando factor: {factor}")
                try:
                    # Insertar factor directamente
                    with db.conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO Factor (Nombre, dimension_nombre) VALUES (%s, %s)",
                            (factor, dimension)
                        )
                    print(f"  ✓ Factor '{factor}' insertado correctamente")
                    
                    # Crear una ejecución de prueba para cada factor
                    execution_id = db.crear_ejecucion(
                        dimension=dimension,
                        factor=factor,
                        metrica="TEST",  # Métrica de prueba
                        metodo="TEST"    # Método de prueba
                    )
                    print(f"  ✓ Ejecución creada con ID: {execution_id}")
                    
                except Exception as e:
                    print(f"  ✗ Error al insertar factor '{factor}': {e}")

        print("\n¡Proceso completado!")
        
    except Exception as e:
        print(f"Error durante la inserción: {e}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    insert_dimensions_and_factors() 