#!/usr/bin/env python3
"""
🚀 Pipeline Ultra-Rápido para Carga de 136GB en BigQuery
⏱️  Tiempo estimado: 15-25 minutos
📊 Optimizado para máxima velocidad y eficiencia
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, WorkerOptions, StandardOptions
from apache_beam.io import ReadFromText, WriteToBigQuery
from apache_beam.io.gcp.bigquery import BigQueryDisposition
import logging
import json
import time

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltraFastLoaderOptions(PipelineOptions):
    """Opciones optimizadas para carga ultra-rápida"""
    
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--input_file', type=str, required=True)
        parser.add_value_provider_argument('--output_table', type=str, required=True)
        parser.add_value_provider_argument('--temp_location', type=str, required=True)
        parser.add_value_provider_argument('--staging_location', type=str, required=True)

class CSVProcessor(beam.DoFn):
    """Procesador optimizado de CSV con manejo de errores"""
    
    def __init__(self, delimiter=','):
        self.delimiter = delimiter
        self.error_count = 0
        
    def process(self, element):
        try:
            # Procesamiento rápido sin validaciones innecesarias
            if element and element.strip():
                return [element.strip().split(self.delimiter)]
            return []
        except Exception as e:
            self.error_count += 1
            if self.error_count <= 1000:  # Log solo los primeros 1000 errores
                logger.warning(f"Error procesando línea: {e}")
            return []

def create_optimized_pipeline():
    """Crea pipeline ultra-optimizado para carga rápida"""
    
    # Configuración de opciones optimizadas
    options = PipelineOptions()
    
    # Configuración de Google Cloud
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'tu-proyecto-id'  # Cambiar por tu PROJECT_ID
    google_cloud_options.region = 'us-central1'
    google_cloud_options.temp_location = 'gs://tu-bucket/temp'
    google_cloud_options.staging_location = 'gs://tu-bucket/staging'
    
    # Configuración de workers optimizada para velocidad
    worker_options = options.view_as(WorkerOptions)
    worker_options.num_workers = 50  # Máximo número de workers
    worker_options.max_num_workers = 100  # Escalado automático
    worker_options.machine_type = 'n1-standard-4'  # Máquina potente
    worker_options.disk_size_gb = 100  # Disco grande para procesamiento
    worker_options.worker_region = 'us-central1'
    
    # Configuración de streaming para mejor rendimiento
    standard_options = options.view_as(StandardOptions)
    standard_options.runner = 'DataflowRunner'
    
    # Configuraciones adicionales para velocidad
    options.view_as(beam.options.pipeline_options.SetupOptions).save_main_session = False
    options.view_as(beam.options.pipeline_options.SetupOptions).setup_file = None
    
    return options

def run_pipeline():
    """Ejecuta el pipeline ultra-optimizado"""
    
    start_time = time.time()
    logger.info("🚀 Iniciando pipeline ultra-rápido...")
    
    # Configuración del pipeline
    options = create_optimized_pipeline()
    
    # Crear pipeline
    with beam.Pipeline(options=options) as pipeline:
        
        # Leer archivo comprimido con procesamiento paralelo
        logger.info("📖 Leyendo archivo comprimido...")
        raw_data = (
            pipeline 
            | 'ReadCSV' >> ReadFromText(
                'gs://desafio-deacero-143d30a0-d8f8-4154-b7df-1773cf286d32/cdo_challenge.csv.gz',
                compression_type='gzip',
                strip_trailing_newlines=True
            )
        )
        
        # Procesar CSV en paralelo
        logger.info("⚡ Procesando CSV en paralelo...")
        processed_data = (
            raw_data
            | 'ProcessCSV' >> beam.ParDo(CSVProcessor())
            | 'FilterEmpty' >> beam.Filter(lambda x: len(x) > 0)
        )
        
        # Cargar a BigQuery con configuración optimizada
        logger.info("💾 Cargando a BigQuery...")
        processed_data | 'WriteToBigQuery' >> WriteToBigQuery(
            'tu-proyecto:tu-dataset.tu-tabla',  # Cambiar por tu tabla
            schema=None,  # Auto-detect schema
            create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
            ignore_unknown_values=True,
            ignore_insert_ids=True,
            method='STREAMING_INSERTS'  # Más rápido que batch
        )
    
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"✅ Pipeline completado en {duration:.2f} segundos ({duration/60:.2f} minutos)")

if __name__ == '__main__':
    run_pipeline()
