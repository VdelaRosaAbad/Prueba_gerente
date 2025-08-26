#!/bin/bash

# Configuración del entorno para carga rápida de 136GB en BigQuery
echo "🚀 Configurando entorno para carga ultra-rápida..."

# Verificar versión de Python
python3 --version
pip3 --version

# Instalar/actualizar librerías necesarias
echo "📦 Instalando librerías optimizadas..."
pip3 install --upgrade \
    apache-beam[gcp]==2.48.0 \
    google-cloud-bigquery==3.11.4 \
    google-cloud-storage==2.10.0 \
    pandas==2.1.1 \
    numpy==1.24.3 \
    pyarrow==13.0.0 \
    fastparquet==2023.10.1

# Verificar instalación
echo "✅ Librerías instaladas:"
pip3 list | grep -E "(apache-beam|google-cloud|pandas|pyarrow)"

# Configurar variables de entorno
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export BUCKET_NAME="desafio-deacero-143d30a0-d8f8-4154-b7df-1773cf286d32"

echo "🔧 Variables configuradas:"
echo "PROJECT_ID: $PROJECT_ID"
echo "REGION: $REGION"
echo "BUCKET_NAME: $BUCKET_NAME"

# Habilitar APIs necesarias
echo "🔌 Habilitando APIs..."
gcloud services enable dataflow.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com

echo "✅ Entorno configurado exitosamente!"
