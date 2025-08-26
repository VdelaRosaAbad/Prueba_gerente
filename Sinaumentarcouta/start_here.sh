#!/bin/bash

# 🚀 INICIO RÁPIDO - SOLUCIONES SIN AUMENTAR CUOTAS
# 💡 Guía paso a paso para cargar 136GB con tus cuotas actuales

echo "🚫 SOLUCIONES SIN AUMENTAR CUOTAS"
echo "=================================="
echo "💡 Esta carpeta contiene soluciones que funcionan con tus 8 IPs disponibles"
echo ""

# Verificar que estamos en la carpeta correcta
if [ ! -f "ultra_optimized_8ips.py" ]; then
    echo "❌ Error: Ejecuta este script desde la carpeta 'Sinaumentarcouta'"
    echo "💡 Comando: cd Sinaumentarcouta && ./start_here.sh"
    exit 1
fi

echo "🔍 VERIFICANDO TU ENTORNO..."
echo ""

# Verificar proyecto configurado
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No hay proyecto configurado"
    echo "💡 Ejecuta: gcloud config set project TU_PROJECT_ID"
    exit 1
else
    echo "✅ Proyecto: $PROJECT_ID"
fi

# Verificar región
REGION=$(gcloud config get-value compute/region 2>/dev/null)
if [ -z "$REGION" ]; then
    echo "⚠️  Región no configurada, usando us-central1 por defecto"
    REGION="us-central1"
else
    echo "✅ Región: $REGION"
fi

echo ""
echo "🎯 OPCIONES DISPONIBLES:"
echo "========================"
echo ""
echo "1️⃣  🚀 PIPELINE ULTRA-OPTIMIZADO (RECOMENDADO)"
echo "    ⏱️  Tiempo: 35-45 minutos"
echo "    💰 Costo: $3-6 USD"
echo "    📊 Workers: 7-8 (dentro de tus cuotas)"
echo "    🎯 Máximo rendimiento posible"
echo ""
echo "2️⃣  📊 CARGA DIRECTA A BIGQUERY"
echo "    ⏱️  Tiempo: 2-4 horas"
echo "    💰 Costo: $0.5-1 USD"
echo "    🚫 Sin Dataflow (solo BigQuery)"
echo "    ✅ Sin restricciones de cuotas"
echo ""
echo "3️⃣  🔧 VERIFICAR CUOTAS Y DIAGNÓSTICO"
echo "    📊 Análisis de tu configuración"
echo "    🎯 Recomendaciones personalizadas"
echo "    🔍 Identificar problemas"
echo ""

# Función para mostrar menú
show_menu() {
    echo ""
    echo "🚀 ¿QUÉ QUIERES HACER?"
    echo "======================="
    echo "1) Ejecutar Pipeline Ultra-Optimizado (35-45 min)"
    echo "2) Carga Directa a BigQuery (2-4 horas)"
    echo "3) Verificar Cuotas y Diagnóstico"
    echo "4) Ver README Completo"
    echo "5) Salir"
    echo ""
    read -p "Selecciona una opción (1-5): " choice
}

# Función para ejecutar pipeline optimizado
run_optimized_pipeline() {
    echo ""
    echo "🚀 EJECUTANDO PIPELINE ULTRA-OPTIMIZADO..."
    echo "⏱️  Tiempo estimado: 35-45 minutos"
    echo "💡 Configurado para máximo rendimiento con 8 IPs"
    echo ""
    
    # Verificar que el script existe
    if [ -f "run_8ips_optimized.sh" ]; then
        chmod +x run_8ips_optimized.sh
        ./run_8ips_optimized.sh
    else
        echo "❌ Error: No se encontró run_8ips_optimized.sh"
    fi
}

# Función para ejecutar carga directa
run_direct_load() {
    echo ""
    echo "📊 EJECUTANDO CARGA DIRECTA A BIGQUERY..."
    echo "⏱️  Tiempo estimado: 2-4 horas"
    echo "💡 Alternativa sin Dataflow"
    echo ""
    
    if [ -f "bigquery_direct_load.py" ]; then
        python3 bigquery_direct_load.py
    else
        echo "❌ Error: No se encontró bigquery_direct_load.py"
    fi
}

# Función para verificar cuotas
check_quotas() {
    echo ""
    echo "🔍 VERIFICANDO CUOTAS Y DIAGNÓSTICO..."
    echo "📊 Análisis de tu configuración actual"
    echo ""
    
    if [ -f "check_quotas.py" ]; then
        python3 check_quotas.py
    else
        echo "❌ Error: No se encontró check_quotas.py"
    fi
}

# Función para mostrar README
show_readme() {
    echo ""
    echo "📚 MOSTRANDO README COMPLETO..."
    echo "================================"
    echo ""
    
    if [ -f "README.md" ]; then
        cat README.md
    else
        echo "❌ Error: No se encontró README.md"
    fi
}

# Bucle principal del menú
while true; do
    show_menu
    
    case $choice in
        1)
            run_optimized_pipeline
            ;;
        2)
            run_direct_load
            ;;
        3)
            check_quotas
            ;;
        4)
            show_readme
            ;;
        5)
            echo ""
            echo "👋 ¡Hasta luego! Recuerda:"
            echo "💡 Para máxima velocidad: Opción 1"
            echo "💡 Para máxima economía: Opción 2"
            echo "💡 Para diagnóstico: Opción 3"
            exit 0
            ;;
        *)
            echo "❌ Opción inválida. Selecciona 1-5"
            ;;
    esac
    
    echo ""
    read -p "Presiona Enter para continuar..."
done
