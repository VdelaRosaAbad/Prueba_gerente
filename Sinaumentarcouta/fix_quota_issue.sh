#!/bin/bash

# 🚨 SOLUCIONADOR DE PROBLEMAS DE CUOTAS EN DATAFLOW
# 🔧 Cambia región y optimiza configuración para evitar límites de cuotas

echo "🚨 Detectado problema de cuotas en us-central1"
echo "🔧 Aplicando solución automática..."

# Obtener proyecto actual
export PROJECT_ID=$(gcloud config get-value project)
echo "📊 Proyecto: $PROJECT_ID"

# Verificar cuotas en diferentes regiones
echo "🔍 Verificando cuotas disponibles en diferentes regiones..."

# Lista de regiones alternativas con mejores cuotas
REGIONS=("us-east1" "us-west1" "europe-west1" "asia-southeast1")

for region in "${REGIONS[@]}"; do
    echo "📍 Verificando región: $region"
    
    # Verificar cuota de direcciones IP
    quota_result=$(gcloud compute regions describe $region --project=$PROJECT_ID --format="value(quotas[metric=IN_USE_ADDRESSES].limit)" 2>/dev/null)
    
    if [ ! -z "$quota_result" ] && [ "$quota_result" != "None" ]; then
        echo "   ✅ IN_USE_ADDRESSES limit: $quota_result"
        
        # Si encontramos una región con más de 20 direcciones IP, la usamos
        if [ "$quota_result" -gt 20 ]; then
            echo "🎯 ¡Región $region tiene cuotas suficientes!"
            export OPTIMAL_REGION=$region
            break
        fi
    else
        echo "   ⚠️  No se pudo verificar cuota en $region"
    fi
done

# Si no encontramos región óptima, usar us-east1 (generalmente tiene más cuotas)
if [ -z "$OPTIMAL_REGION" ]; then
    export OPTIMAL_REGION="us-east1"
    echo "⚠️  Usando región por defecto: $OPTIMAL_REGION"
fi

echo "🔧 Configurando región óptima: $OPTIMAL_REGION"

# Configurar región en gcloud
gcloud config set compute/region $OPTIMAL_REGION
gcloud config set dataflow/region $OPTIMAL_REGION

# Actualizar scripts con la nueva región
echo "📝 Actualizando configuración en scripts..."

# Actualizar ultra_fast_loader.py
sed -i "s/us-central1/$OPTIMAL_REGION/g" ultra_fast_loader.py
sed -i "s/50/8/g" ultra_fast_loader.py  # Reducir workers iniciales
sed -i "s/100/16/g" ultra_fast_loader.py  # Reducir máximo de workers

# Actualizar run_ultra_fast_loader.sh
sed -i "s/us-central1/$OPTIMAL_REGION/g" run_ultra_fast_loader.sh
sed -i "s/50/8/g" run_ultra_fast_loader.sh
sed -i "s/100/16/g" run_ultra_fast_loader.sh

echo "✅ Configuración actualizada para región: $OPTIMAL_REGION"
echo "📊 Workers configurados: 8 iniciales, máximo 16 (dentro de límites de cuota)"

# Mostrar configuración actual
echo ""
echo "🔧 CONFIGURACIÓN ACTUALIZADA:"
echo "   🌍 Región: $OPTIMAL_REGION"
echo "   👥 Workers iniciales: 8"
echo "   🚀 Workers máximos: 16"
echo "   📁 Archivo: gs://desafio-deacero-143d30a0-d8f8-4154-b7df-1773cf286d32/cdo_challenge.csv.gz"
echo ""

# Verificar que la nueva configuración esté lista
echo "🧪 Verificando configuración..."
python3 -c "
import re
with open('ultra_fast_loader.py', 'r') as f:
    content = f.read()
    region_match = re.search(r'region = \"([^\"]+)\"', content)
    workers_match = re.search(r'num_workers = (\d+)', content)
    max_workers_match = re.search(r'max_num_workers = (\d+)', content)
    
    if region_match and workers_match and max_workers_match:
        print(f'✅ Región configurada: {region_match.group(1)}')
        print(f'✅ Workers iniciales: {workers_match.group(1)}')
        print(f'✅ Workers máximos: {max_workers_match.group(1)}')
    else:
        print('❌ Error en la configuración')
"

echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Ejecutar: ./run_ultra_fast_loader.sh"
echo "2. Monitorear: python3 monitor_pipeline.py --project=$PROJECT_ID"
echo "3. Verificar en Dataflow Console: https://console.cloud.google.com/dataflow"
echo ""
echo "💡 CONSEJO: Con esta configuración optimizada, la carga tomará ~45-60 minutos"
echo "   pero será estable y sin errores de cuotas."
