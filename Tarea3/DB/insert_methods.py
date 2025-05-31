import psycopg
from db_operations import DBOperations

def insert_methods():
    try:
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
                "metodo_id": "NoDuplicacion-LeveshteinDistance",
                "metodo_aplicado_id": "NoDuplicacion-LeveshteinDistance_ap",
                "metrica_id": "NoDuplicación-CantDups"
            },
            {
                "metodo_id": "NoDuplicación-CantDups-Contar",
                "metodo_aplicado_id": "NoDuplicación-CantDups-Contar_ap",
                "metrica_id": "NoDuplicación-CantDups"
            },
            {
                "metodo_id": "IntDominio-OutBounds-Gen-ContarNum",
                "metodo_aplicado_id": "IntDominio-OutBounds-Gen-ContarNum_ap",
                "metrica_id": "IntDominio-OutBounds-Gen"
            }
        ]

        # Conectar a la base de datos
        db = DBOperations()
        
        print("Iniciando inserción de métodos...")
        
        # Insertar cada método y su método aplicado
        for method in methods_data:
            print(f"\nInsertando método: {method['metodo_id']}")
            try:
                # Insertar método
                with db.conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Metodo (id_metodo, metrica_id) VALUES (%s, %s)",
                        (method['metodo_id'], method['metrica_id'])
                    )
                print(f"✓ Método '{method['metodo_id']}' insertado correctamente")
                
                # Insertar método aplicado
                with db.conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO MetodoAplicado (id_metodo_aplicado, metodo_id) VALUES (%s, %s)",
                        (method['metodo_aplicado_id'], method['metodo_id'])
                    )
                print(f"✓ Método aplicado '{method['metodo_aplicado_id']}' insertado correctamente")
                
            except Exception as e:
                print(f"✗ Error al insertar método '{method['metodo_id']}': {e}")

        print("\n¡Proceso completado!")
        
    except Exception as e:
        print(f"Error durante la inserción: {e}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    insert_methods() 