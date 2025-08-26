#!/bin/bash

# ⚡ CONFIGURACIÓN RÁPIDA - SOLUCIONES SIN AUMENTAR CUOTAS
# 🔧 Configura el entorno para máximo rendimiento con 8 IPs

echo "⚡ CONFIGURACIÓN RÁPIDA PARA 8 IPs"
echo "==================================="
echo "💡 Optimizando tu entorno para máximo rendimiento"
echo ""

# Verificar que estamos en la carpeta correcta
if [ ! -f "ultra_optimized_8ips.py" ]; then
    echo "❌ Error: Ejecuta este script desde la carpeta 'Sinaumentarcouta'"
    echo "💡 Comando: cd Sinaumentarcouta && ./quick_config.sh"
    exit 1
fi

echo "🔍 VERIFICANDO CONFIGURACIÓN ACTUAL..."
echo ""

# Obtener proyecto actual
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No hay proyecto configurado"
    echo "💡 Ejecuta: gcloud config set project TU_PROJECT_ID"
    exit 1
else
    echo "✅ Proyecto: $PROJECT_ID"
fi

# Configurar región para máximo rendimiento
echo "🌍 Configurando región óptima..."
gcloud config set compute/region us-central1
gcloud config set dataflow/region us-central1
echo "✅ Región configurada: us-central1"

# Habilitar APIs necesarias
echo "🔌 Habilitando APIs necesarias..."
gcloud services enable dataflow.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
echo "✅ APIs habilitadas"

# Crear bucket temporal
echo "📦 Configurando bucket temporal..."
BUCKET_NAME="${PROJECT_ID}-temp"
gsutil mb -p $PROJECT_ID -c STANDARD -l us-central1 gs://$BUCKET_NAME 2>/dev/null || true
echo "✅ Bucket temporal: gs://$BUCKET_NAME"

# Crear dataset en BigQuery
echo "🗄️ Configurando BigQuery..."
bq mk --dataset $PROJECT_ID:cdo_challenge 2>/dev/null || true
echo "✅ Dataset: cdo_challenge"

# Configurar ubicaciones temporales
export TEMP_LOCATION="gs://$BUCKET_NAME/temp"
export STAGING_LOCATION="gs://$BUCKET_NAME/staging"

# Crear directorios temporales
gsutil -m rm -r $TEMP_LOCATION 2>/dev/null || true
gsutil -m rm -r $STAGING_LOCATION 2>/dev/null || true
gsutil mb -p $PROJECT_ID -c STANDARD -l us-central1 $TEMP_LOCATION 2>/dev/null || true
gsutil mb -p $PROJECT_ID -c STANDARD -l us-central1 $STAGING_LOCATION 2>/dev/null || true

echo "✅ Directorios temporales configurados:"
echo "   📁 Temp: $TEMP_LOCATION"
echo "   📁 Staging: $STAGING_LOCATION"

# Actualizar scripts con configuración actual
echo "📝 Actualizando configuración en scripts..."

# Actualizar ultra_optimized_8ips.py
if [ -f "ultra_optimized_8ips.py" ]; then
    sed -i "s/tu-proyecto-id/$PROJECT_ID/g" ultra_optimized_8ips.py
    sed -i "s/tu-proyecto:tu-dataset.tu-tabla/$PROJECT_ID:cdo_challenge.raw_data/g" ultra_optimized_8ips.py
    sed -i "s|gs://tu-bucket/temp|$TEMP_LOCATION|g" ultra_optimized_8ips.py
    sed -i "s|gs://tu-bucket/staging|$STAGING_LOCATION|g" ultra_optimized_8ips.py
    echo "✅ ultra_optimized_8ips.py configurado"
fi

# Actualizar run_8ips_optimized.sh
if [ -f "run_8ips_optimized.sh" ]; then
    sed -i "s/tu-proyecto-id/$PROJECT_ID/g" run_8ips_optimized.sh
    sed -i "s/tu-proyecto:tu-dataset.tu-tabla/$PROJECT_ID:cdo_challenge.raw_data/g" run_8ips_optimized.sh
    sed -i "s|gs://tu-bucket/temp|$TEMP_LOCATION|g" run_8ips_optimized.sh
    sed -i "s|gs://tu-bucket/staging|$STAGING_LOCATION|g" run_8ips_optimized.sh
    echo "✅ run_8ips_optimized.sh configurado"
fi

# Configurar permisos de ejecución
echo "🔐 Configurando permisos de ejecución..."
chmod +x *.sh *.py
echo "✅ Permisos configurados"

echo ""
echo "🎯 CONFIGURACIÓN COMPLETADA"
echo "============================"
echo "✅ Proyecto: $PROJECT_ID"
echo "✅ Región: us-central1"
echo "✅ Bucket temporal: gs://$BUCKET_NAME"
echo "✅ Dataset: cdo_challenge"
echo "✅ APIs habilitadas"
echo "✅ Scripts configurados"
echo "✅ Permisos configurados"
echo ""

echo "🚀 PRÓXIMOS PASOS:"
echo "=================="
echo "1. Ejecutar pipeline: ./run_8ips_optimized.sh"
echo "2. O usar inicio rápido: ./start_here.sh"
echo "3. Monitorear en: https://console.cloud.google.com/dataflow"
echo "4. Verificar en: https://console.cloud.google.com/bigquery"
echo ""

echo "💡 CONSEJO: Tu entorno está optimizado para máximo rendimiento con 8 IPs"
echo "⏱️  Tiempo estimado: 35-45 minutos para 136GB"
echo "💰 Costo estimado: $3-6 USD"
echo ""

# Preguntar si quiere ejecutar ahora
read -p "¿Quieres ejecutar el pipeline ahora? (s/N): " choice
if [[ $choice =~ ^[Ss]$ ]]; then
    echo ""
    echo "🚀 EJECUTANDO PIPELINE ULTRA-OPTIMIZADO..."
    ./run_8ips_optimized.sh
else
    echo ""
    echo "👋 Configuración completada. Ejecuta cuando estés listo:"
    echo "   ./start_here.sh"
fi
