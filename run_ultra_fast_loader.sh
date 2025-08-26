#!/bin/bash

# 🚀 Script de Ejecución Automatizada para Carga Ultra-Rápida
# ⏱️  Tiempo estimado: 15-25 minutos para 136GB

set -e

echo "🚀 Iniciando carga ultra-rápida de 136GB en BigQuery..."
echo "⏰ Inicio: $(date)"

# Configurar variables de entorno
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export BUCKET_NAME="desafio-deacero-143d30a0-d8f8-4154-b7df-1773cf286d32"
export DATASET_NAME="cdo_challenge"
export TABLE_NAME="raw_data"

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

echo "🔧 Variables configuradas:"
echo "PROJECT_ID: $PROJECT_ID"
echo "REGION: $REGION"
echo "BUCKET_NAME: $BUCKET_NAME"
echo "DATASET: $DATASET_NAME"
echo "TABLA: $TABLE_NAME"
echo "TEMP_LOCATION: $TEMP_LOCATION"
echo "STAGING_LOCATION: $STAGING_LOCATION"

# Actualizar el script Python con las variables correctas
echo "📝 Actualizando configuración del pipeline..."
sed -i "s/tu-proyecto-id/$PROJECT_ID/g" ultra_fast_loader.py
sed -i "s/tu-proyecto:tu-dataset.tu-tabla/$PROJECT_ID:$DATASET_NAME.$TABLE_NAME/g" ultra_fast_loader.py
sed -i "s|gs://tu-bucket/temp|$TEMP_LOCATION|g" ultra_fast_loader.py
sed -i "s|gs://tu-bucket/staging|$STAGING_LOCATION|g" ultra_fast_loader.py

# Ejecutar pipeline optimizado
echo "🚀 Ejecutando pipeline ultra-rápido..."
python3 ultra_fast_loader.py \
    --project=$PROJECT_ID \
    --region=$REGION \
    --temp_location=$TEMP_LOCATION \
    --staging_location=$STAGING_LOCATION \
    --runner=DataflowRunner \
    --num_workers=50 \
    --max_num_workers=100 \
    --machine_type=n1-standard-4 \
    --disk_size_gb=100 \
    --worker_region=$REGION \
    --setup_file=./setup.py \
    --save_main_session=False

echo "✅ Pipeline completado!"
echo "⏰ Fin: $(date)"

# Limpiar recursos temporales
echo "🧹 Limpiando recursos temporales..."
gsutil -m rm -r $TEMP_LOCATION 2>/dev/null || true
gsutil -m rm -r $STAGING_LOCATION 2>/dev/null || true

echo "🎉 ¡Carga completada exitosamente!"
