#!/bin/bash

# 🚀 Script de Ejecución para 8 IPs (Sin Aumentar Cuotas)
# ⏱️  Tiempo estimado: 35-45 minutos para 136GB
# 💡 Optimizado para máximo rendimiento con restricción de cuotas

set -e

echo "🚀 Iniciando carga optimizada para 8 IPs (sin aumentar cuotas)..."
echo "⏰ Inicio: $(date)"
echo "💡 Esta solución funciona con tus cuotas actuales"

# Configurar variables de entorno
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"  # Mantener tu región actual
export BUCKET_NAME="desafio-deacero-143d30a0-d8f8-4154-b7df-1773cf286d32"
export DATASET_NAME="cdo_challenge"
export TABLE_NAME="raw_data"

echo "🔧 Configuración actual:"
echo "   📊 Proyecto: $PROJECT_ID"
echo "   🌍 Región: $REGION (con cuota de 8 IPs)"
echo "   📁 Archivo: gs://$BUCKET_NAME/cdo_challenge.csv.gz"
echo "   🗄️ Dataset: $DATASET_NAME"
echo "   📋 Tabla: $TABLE_NAME"

# Crear bucket temporal si no existe
echo "📦 Configurando bucket temporal..."
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION gs://$PROJECT_ID-temp 2>/dev/null || true

# Crear dataset y tabla en BigQuery
echo "🗄️ Configurando BigQuery..."
bq mk --dataset $PROJECT_ID:$DATASET_NAME 2>/dev/null || true

# Configurar ubicaciones temporales
export TEMP_LOCATION="gs://$PROJECT_ID-temp/temp"
export STAGING_LOCATION="gs://$PROJECT_ID-temp/staging"

# Crear directorios temporales
gsutil -m rm -r $TEMP_LOCATION 2>/dev/null || true
gsutil -m rm -r $STAGING_LOCATION 2>/dev/null || true
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION $TEMP_LOCATION 2>/dev/null || true
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION $STAGING_LOCATION 2>/dev/null || true

echo "✅ Recursos temporales configurados:"
echo "   📁 Temp: $TEMP_LOCATION"
echo "   📁 Staging: $STAGING_LOCATION"

# Actualizar el script Python con las variables correctas
echo "📝 Actualizando configuración del pipeline..."
sed -i "s/tu-proyecto-id/$PROJECT_ID/g" ultra_optimized_8ips.py
sed -i "s/tu-proyecto:tu-dataset.tu-tabla/$PROJECT_ID:$DATASET_NAME.$TABLE_NAME/g" ultra_optimized_8ips.py
sed -i "s|gs://tu-bucket/temp|$TEMP_LOCATION|g" ultra_optimized_8ips.py
sed -i "s|gs://tu-bucket/staging|$STAGING_LOCATION|g" ultra_optimized_8ips.py

echo "🚀 Ejecutando pipeline ultra-optimizado para 8 IPs..."
echo "📊 Configuración: 7 workers, máquina n1-standard-16, disco 500GB"

# Ejecutar pipeline optimizado para 8 IPs
python3 ultra_optimized_8ips.py \
    --project=$PROJECT_ID \
    --region=$REGION \
    --temp_location=$TEMP_LOCATION \
    --staging_location=$STAGING_LOCATION \
    --runner=DataflowRunner \
    --num_workers=7 \
    --max_num_workers=8 \
    --machine_type=n1-standard-16 \
    --disk_size_gb=500 \
    --worker_region=$REGION \
    --setup_file=./setup.py \
    --save_main_session=False

echo "✅ Pipeline completado!"
echo "⏰ Fin: $(date)"

# Limpiar recursos temporales
echo "🧹 Limpiando recursos temporales..."
gsutil -m rm -r $TEMP_LOCATION 2>/dev/null || true
gsutil -m rm -r $STAGING_LOCATION 2>/dev/null || true

echo ""
echo "🎉 ¡Carga completada exitosamente SIN aumentar cuotas!"
echo "📊 Datos disponibles en: $PROJECT_ID:$DATASET_NAME.$TABLE_NAME"
echo ""
echo "💡 CONSEJOS:"
echo "   • Monitorea en: https://console.cloud.google.com/dataflow"
echo "   • Verifica en: https://console.cloud.google.com/bigquery"
echo "   • Para futuras cargas, usa: python3 ultra_optimized_8ips.py"
