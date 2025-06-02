import os
import sys
import subprocess
import time

def run_script(script_path):
    """
    Ejecuta un script Python y maneja cualquier error que pueda ocurrir.
    """
    try:
        print(f"\n{'='*20} Ejecutando {os.path.basename(script_path)} {'='*20}")
        
        # Ejecutar el script usando subprocess
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True)
        
        # Imprimir la salida del script
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"\n{'='*20} {os.path.basename(script_path)} completado exitosamente {'='*20}")
            return True
        else:
            print(f"\nError en {os.path.basename(script_path)} con código de salida: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\nError ejecutando {os.path.basename(script_path)}: {str(e)}")
        return False

def main():
    # Obtener el directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lista de scripts a ejecutar (excluyendo run_all_tests.py y levenshteinTest.py)
    scripts = [
        'Precision-Fechas.py',
        'intInterRelPertenencia.py',
        'intBoundsGenContarNum.py',
        'cantDupsContar.py',
        'gradoContar.py',
        'reglaCorrectaISBN.py'
    ]
    
    # Contador de scripts exitosos y fallidos
    successful = 0
    failed = 0
    
    # Ejecutar cada script
    for script in scripts:
        script_path = os.path.join(current_dir, script)
        if run_script(script_path):
            successful += 1
        else:
            failed += 1
    
    # Mostrar resumen
    print(f"\n{'='*20} Resumen de ejecución {'='*20}")
    print(f"Scripts ejecutados exitosamente: {successful}")
    print(f"Scripts con errores: {failed}")
    print(f"Total de scripts ejecutados: {len(scripts)}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"\nTiempo total de ejecución: {end_time - start_time:.2f} segundos") 