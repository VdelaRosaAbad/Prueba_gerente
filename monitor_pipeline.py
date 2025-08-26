#!/usr/bin/env python3
"""
📊 Monitor de Pipeline en Tiempo Real
🔍 Monitorea el progreso y rendimiento del pipeline de Dataflow
"""

import time
import subprocess
import json
from datetime import datetime, timedelta
import argparse

def get_pipeline_status(project_id, job_id=None):
    """Obtiene el estado del pipeline de Dataflow"""
    try:
        if job_id:
            cmd = f"gcloud dataflow jobs describe {job_id} --project={project_id} --format=json"
        else:
            cmd = f"gcloud dataflow jobs list --project={project_id} --format=json --limit=5"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Error obteniendo estado: {e}")
        return None

def get_bigquery_stats(project_id, dataset, table):
    """Obtiene estadísticas de BigQuery"""
    try:
        cmd = f"bq show --format=json {project_id}:{dataset}.{table}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Error obteniendo stats de BigQuery: {e}")
        return None

def monitor_pipeline(project_id, dataset="cdo_challenge", table="raw_data", interval=30):
    """Monitorea el pipeline continuamente"""
    
    print("🔍 Iniciando monitoreo del pipeline...")
    print(f"📊 Proyecto: {project_id}")
    print(f"🗄️ Dataset: {dataset}")
    print(f"📋 Tabla: {table}")
    print(f"⏱️  Intervalo de monitoreo: {interval} segundos")
    print("-" * 60)
    
    start_time = datetime.now()
    last_row_count = 0
    
    while True:
        try:
            current_time = datetime.now()
            elapsed = current_time - start_time
            
            # Obtener estado del pipeline
            pipeline_status = get_pipeline_status(project_id)
            if pipeline_status:
                if isinstance(pipeline_status, list) and pipeline_status:
                    latest_job = pipeline_status[0]
                    job_id = latest_job.get('id', 'N/A')
                    state = latest_job.get('currentState', 'N/A')
                    creation_time = latest_job.get('creationTime', 'N/A')
                    
                    print(f"⏰ {current_time.strftime('%H:%M:%S')} | 🆔 Job: {job_id[:8]}... | 📊 Estado: {state}")
                    
                    # Obtener estadísticas de BigQuery
                    bq_stats = get_bigquery_stats(project_id, dataset, table)
                    if bq_stats:
                        current_rows = bq_stats.get('numRows', 0)
                        current_size = bq_stats.get('numBytes', 0)
                        
                        if current_rows > last_row_count:
                            rows_added = current_rows - last_row_count
                            print(f"   📈 Filas en BigQuery: {current_rows:,} (+{rows_added:,})")
                            print(f"   💾 Tamaño: {current_size / (1024**3):.2f} GB")
                            last_row_count = current_rows
                        
                        # Calcular velocidad de procesamiento
                        if elapsed.total_seconds() > 0:
                            rows_per_second = current_rows / elapsed.total_seconds()
                            print(f"   🚀 Velocidad: {rows_per_second:.0f} filas/segundo")
            
            print(f"   ⏱️  Tiempo transcurrido: {str(elapsed).split('.')[0]}")
            print("-" * 60)
            
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoreo detenido por el usuario")
            break
        except Exception as e:
            print(f"❌ Error en monitoreo: {e}")
            time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="Monitor de Pipeline Dataflow")
    parser.add_argument("--project", required=True, help="ID del proyecto de GCP")
    parser.add_argument("--dataset", default="cdo_challenge", help="Nombre del dataset")
    parser.add_argument("--table", default="raw_data", help="Nombre de la tabla")
    parser.add_argument("--interval", type=int, default=30, help="Intervalo de monitoreo en segundos")
    
    args = parser.parse_args()
    
    monitor_pipeline(args.project, args.dataset, args.table, args.interval)

if __name__ == "__main__":
    main()
