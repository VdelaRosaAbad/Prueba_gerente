# 🚀 Cargador Ultra-Rápido para BigQuery

## ⚡ Carga de 136GB en menos de 30 minutos

Solución optimizada para cargar archivos masivos en BigQuery utilizando Dataflow, Python y Cloud Shell.

## 🎯 Características Principales

- **⚡ Velocidad Ultra-Rápida**: Carga de 136GB en 15-25 minutos
- **🔄 Procesamiento Paralelo**: Utiliza hasta 100 workers de Dataflow
- **📊 Monitoreo en Tiempo Real**: Seguimiento del progreso y rendimiento
- **🔧 Configuración Automatizada**: Setup automático del entorno
- **💰 Optimización de Costos**: Configuración balanceada entre velocidad y costo

## 🛠️ Requisitos Previos

- ✅ Proyecto de Google Cloud Platform activo
- ✅ Cloud Shell habilitado
- ✅ APIs de Dataflow, BigQuery y Storage habilitadas
- ✅ Permisos de administrador o editor en el proyecto

## 🚀 Instalación y Configuración

### Paso 1: Clonar y Configurar

```bash
# En Cloud Shell, ejecutar:
chmod +x *.sh
chmod +x *.py

# Configurar el entorno
./setup_environment.sh
```

### Paso 2: Verificar Configuración

```bash
# Verificar que las librerías estén instaladas
python3 -c "import apache_beam; print('✅ Apache Beam instalado')"
python3 -c "import google.cloud.bigquery; print('✅ BigQuery instalado')"

# Verificar configuración de GCP
gcloud config list
```

## 🎮 Uso

### Opción 1: Ejecución Automatizada (Recomendada)

```bash
# Ejecutar todo el proceso automáticamente
./run_ultra_fast_loader.sh
```

### Opción 2: Ejecución Manual

```bash
# 1. Configurar variables
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"

# 2. Ejecutar pipeline
python3 ultra_fast_loader.py \
    --project=$PROJECT_ID \
    --region=$REGION \
    --temp_location=gs://$PROJECT_ID-temp/temp \
    --staging_location=gs://$PROJECT_ID-temp/staging \
    --runner=DataflowRunner \
    --num_workers=50 \
    --max_num_workers=100
```

### Opción 3: Monitoreo en Tiempo Real

```bash
# Monitorear el progreso del pipeline
python3 monitor_pipeline.py --project=$PROJECT_ID
```

## 📊 Monitoreo y Métricas

### Dashboard de Dataflow
- Acceder a: [Dataflow Console](https://console.cloud.google.com/dataflow)
- Ver jobs activos y métricas en tiempo real

### Métricas Clave
- **Velocidad de Procesamiento**: Filas por segundo
- **Uso de Workers**: Número de workers activos
- **Progreso**: Porcentaje de archivo procesado
- **Tiempo Estimado**: Tiempo restante para completar

## ⚙️ Configuración Avanzada

### Optimización de Workers

```python
# En ultra_fast_loader.py, ajustar:
worker_options.num_workers = 50          # Workers iniciales
worker_options.max_num_workers = 100     # Máximo de workers
worker_options.machine_type = 'n1-standard-4'  # Tipo de máquina
```

### Configuración de Región

```bash
# Cambiar región según tu ubicación
export REGION="us-central1"     # Estados Unidos Central
export REGION="europe-west1"    # Europa Occidental
export REGION="asia-southeast1" # Asia Sudeste
```

## 🔍 Solución de Problemas

### Error: "API not enabled"
```bash
# Habilitar APIs necesarias
gcloud services enable dataflow.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
```

### Error: "Insufficient quota"
```bash
# Verificar cuotas disponibles
gcloud compute regions describe us-central1 --project=$PROJECT_ID
```

### Error: "Permission denied"
```bash
# Verificar permisos
gcloud projects get-iam-policy $PROJECT_ID
```

## 📈 Rendimiento Esperado

| Tamaño de Archivo | Workers | Tiempo Estimado | Costo Aproximado |
|-------------------|---------|-----------------|------------------|
| 136 GB            | 50-100  | 15-25 min       | $2-5 USD         |
| 50 GB             | 30-50   | 8-15 min        | $1-3 USD         |
| 10 GB             | 10-20   | 3-8 min         | $0.5-1 USD       |

## 🏗️ Arquitectura de la Solución

```
📁 Archivo CSV.gz (136GB)
    ↓
🌐 Cloud Storage
    ↓
⚡ Dataflow Pipeline (50-100 workers)
    ↓
🗄️ BigQuery Table
    ↓
📊 Datos Disponibles para Análisis
```

## 🔧 Personalización

### Cambiar Formato de Archivo

```python
# En ultra_fast_loader.py, modificar:
raw_data = (
    pipeline 
    | 'ReadFile' >> ReadFromText(
        'gs://tu-bucket/tu-archivo.csv',  # Cambiar ruta
        compression_type='gzip',           # Cambiar compresión
        strip_trailing_newlines=True
    )
)
```

### Cambiar Esquema de BigQuery

```python
# Esquema personalizado en lugar de auto-detect
schema = 'campo1:STRING,campo2:INTEGER,campo3:FLOAT'
processed_data | 'WriteToBigQuery' >> WriteToBigQuery(
    'proyecto:dataset.tabla',
    schema=schema,  # Usar esquema personalizado
    # ... otras opciones
)
```

## 📚 Recursos Adicionales

- [Documentación de Dataflow](https://cloud.google.com/dataflow/docs)
- [Guía de BigQuery](https://cloud.google.com/bigquery/docs)
- [Optimización de Costos](https://cloud.google.com/dataflow/docs/guides/cost-optimization)
- [Monitoreo de Jobs](https://cloud.google.com/dataflow/docs/guides/monitoring)

## 🤝 Soporte

Para problemas o preguntas:
1. Revisar logs del pipeline en Dataflow Console
2. Verificar configuración de permisos y APIs
3. Consultar métricas de rendimiento
4. Revisar cuotas del proyecto

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**⚡ ¡Optimiza tu carga de datos y reduce el tiempo de 136GB de horas a minutos!**
