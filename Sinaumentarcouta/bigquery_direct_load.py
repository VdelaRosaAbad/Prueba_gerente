#!/usr/bin/env python3
"""
📊 Carga Directa a BigQuery (Alternativa a Dataflow)
⏱️  Tiempo estimado: 2-4 horas para 136GB
💡 Funciona SIN Dataflow, solo con BigQuery
🚫 Para cuando no puedes aumentar cuotas de Dataflow
"""

import subprocess
import time
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_bq_load():
    """Ejecuta carga directa a BigQuery usando bq load"""
    
    start_time = time.time()
    logger.info("🚀 Iniciando carga directa a BigQuery...")
    logger.info("💡 Alternativa cuando Dataflow no está disponible")
    
    # Obtener proyecto actual
    try:
        project_id = subprocess.run(
            ['gcloud', 'config', 'get-value', 'project'], 
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except subprocess.CalledProcessError:
        logger.error("❌ No se pudo obtener el proyecto. Ejecuta: gcloud config set project TU_PROJECT_ID")
        return False
    
    logger.info(f"📊 Proyecto: {project_id}")
    
    # Configuración de la carga
    dataset_name = "cdo_challenge"
    table_name = "raw_data"
    source_file = "gs://desafio-deacero-143d30a0-d8f8-4154-b7df-1773cf286d32/cdo_challenge.csv.gz"
    
    # Crear dataset si no existe
    logger.info(f"🗄️ Creando dataset: {dataset_name}")
    try:
        subprocess.run([
            'bq', 'mk', '--dataset', f'{project_id}:{dataset_name}'
        ], check=False)  # No fallar si ya existe
        logger.info("✅ Dataset creado/verificado")
    except Exception as e:
        logger.warning(f"⚠️  Error creando dataset: {e}")
    
    # Comando de carga optimizado
    load_command = [
        'bq', 'load',
        '--source_format=CSV',
        '--autodetect',  # Auto-detect schema
        '--ignore_unknown_values',
        '--max_bad_records=10000',  # Permitir hasta 10k registros malos
        '--replace',  # Reemplazar tabla si existe
        '--field_delimiter=,',
        '--skip_leading_rows=1',  # Saltar encabezado si existe
        '--allow_quoted_newlines',  # Permitir saltos de línea en campos
        '--allow_jagged_rows',  # Permitir filas con diferente número de columnas
        f'{project_id}:{dataset_name}.{table_name}',
        source_file
    ]
    
    logger.info("📤 Iniciando carga directa a BigQuery...")
    logger.info(f"📁 Archivo: {source_file}")
    logger.info(f"📋 Tabla: {project_id}:{dataset_name}.{table_name}")
    
    # Ejecutar carga
    try:
        result = subprocess.run(
            load_command,
            capture_output=True,
            text=True,
            check=True
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info("✅ ¡Carga completada exitosamente!")
        logger.info(f"⏱️  Tiempo total: {duration:.2f} segundos ({duration/60:.2f} minutos)")
        logger.info(f"📊 Datos disponibles en: {project_id}:{dataset_name}.{table_name}")
        
        # Mostrar estadísticas de la tabla
        logger.info("📈 Obteniendo estadísticas de la tabla...")
        stats_result = subprocess.run([
            'bq', 'show', '--format=json', f'{project_id}:{dataset_name}.{table_name}'
        ], capture_output=True, text=True, check=True)
        
        import json
        stats = json.loads(stats_result.stdout)
        num_rows = stats.get('numRows', 0)
        num_bytes = stats.get('numBytes', 0)
        
        logger.info(f"📊 Filas cargadas: {num_rows:,}")
        logger.info(f"💾 Tamaño: {num_bytes / (1024**3):.2f} GB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error en la carga: {e}")
        logger.error(f"📝 Error details: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        return False

def check_bq_availability():
    """Verifica que bq esté disponible"""
    try:
        result = subprocess.run(['bq', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ BigQuery CLI disponible")
            return True
        else:
            logger.error("❌ BigQuery CLI no disponible")
            return False
    except FileNotFoundError:
        logger.error("❌ BigQuery CLI no encontrado. Instala Google Cloud SDK")
        return False

def main():
    """Función principal"""
    logger.info("🔍 VERIFICANDO DISPONIBILIDAD DE BIGQUERY")
    logger.info("=" * 60)
    
    if not check_bq_availability():
        logger.error("❌ No se puede continuar sin BigQuery CLI")
        logger.info("💡 Instala: https://cloud.google.com/sdk/docs/install")
        return False
    
    logger.info("🚀 INICIANDO CARGA DIRECTA A BIGQUERY")
    logger.info("=" * 60)
    logger.info("💡 Esta es una alternativa cuando Dataflow no está disponible")
    logger.info("⏱️  Tiempo estimado: 2-4 horas (más lento que Dataflow)")
    logger.info("✅ Ventaja: Funciona sin restricciones de cuotas")
    logger.info("")
    
    # Confirmar con el usuario
    response = input("¿Continuar con la carga directa? (s/N): ").strip().lower()
    if response not in ['s', 'si', 'sí', 'y', 'yes']:
        logger.info("❌ Carga cancelada por el usuario")
        return False
    
    # Ejecutar carga
    success = run_bq_load()
    
    if success:
        logger.info("")
        logger.info("🎉 ¡CARGA COMPLETADA EXITOSAMENTE!")
        logger.info("💡 Para futuras cargas rápidas, considera:")
        logger.info("   • Solicitar aumento de cuotas de Dataflow")
        logger.info("   • Usar el pipeline optimizado para 8 IPs")
        logger.info("   • Contactar soporte de Google Cloud")
    else:
        logger.error("")
        logger.error("❌ LA CARGA FALLÓ")
        logger.error("💡 Alternativas:")
        logger.error("   • Revisar logs de error arriba")
        logger.error("   • Verificar permisos del proyecto")
        logger.error("   • Usar el pipeline optimizado para 8 IPs")
    
    return success

if __name__ == '__main__':
    main()
