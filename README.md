# CDI Scripts

Este repositorio contiene scripts para el procesamiento y análisis de datos de CDI.

## Requisitos Previos

- Python 3.x
- pip (gestor de paquetes de Python)
- Acceso a la base de datos

## Pasos para la Ejecución

### 1. Preparación de Datos
- Colocar los archivos CSV de L1 y L2 en el directorio raíz del proyecto
- Asegurarse de que los archivos tengan los nombres correctos y el formato adecuado

### 2. Integración Inicial
- Ejecutar los scripts ubicados en la carpeta `Scripts/Initial Integration`
- Estos scripts realizarán el procesamiento inicial de los datos

### 3. Configuración del Entorno
- Crear un archivo `.env` en el directorio raíz del proyecto
- Agregar las siguientes variables de entorno (reemplazar los valores con tus credenciales):
```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

### 4. Inicialización de la Base de Datos
- Ejecutar el script de inicialización de la base de datos:
```bash
python DB/init_db.py
```
Este script realizará las siguientes operaciones:
- Creación de la base de datos
- Creación de las tablas necesarias
- Inserción de datos de dimensiones
- Inserción de métricas
- Inserción de métodos


### 5. Ejecución de Scripts de Tarea 3
- Los scripts de la tarea 3 pueden ejecutarse en cualquier orden
- Cada script guardará sus resultados en la base de datos
- Asegurarse de que la base de datos esté correctamente configurada antes de ejecutar estos scripts 