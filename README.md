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
- Crear un archivo `.env` en el directorio raíz del proyecto (mismo nivel que este README)
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

## Métricas y Calificaciones de Calidad

### Métricas de Calificación Directa (alto % = bueno)
- `ExactSint-ReglaCorrecta-ISBN_ap` (Exactitud Sintáctica)
- `IntDominio-OutBounds-Gen-ContarNum_ap` (Integridad de Dominio)
- `Precision-Fechas_ap` (Precisión)

**Enfoques de evaluación para métricas directas**:
- 0-30%: Mala
- 31-60%: Buena
- 61-90%: Muy buena
- 91-100%: Excelente

### Métricas de Calificación Inversa (bajo % = bueno)
- `Densidad-Grado-Contar_ap` (Densidad)
- `NoDuplicacion-CantDups-Contar_ap` (No Duplicación)
- `IntInterRel-Pertenencia_ap` (Integridad Interrelación)

**Enfoques de evaluación para métricas inversas**:
- 0-30%: Excelente
- 31-60%: Muy buena
- 61-90%: Buena
- 91-100%: Mala

*Nota: Las métricas de calificación directa consideran un alto porcentaje como bueno, mientras que las métricas de calificación inversa consideran un bajo porcentaje como bueno.* 