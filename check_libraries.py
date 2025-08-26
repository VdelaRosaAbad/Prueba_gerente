#!/usr/bin/env python3
"""
🔍 Verificador de Librerías
✅ Verifica que todas las librerías necesarias estén instaladas
📊 Muestra versiones y estado de instalación
"""

import sys
import subprocess
import importlib
from typing import Dict, List, Tuple

# Librerías requeridas con versiones mínimas
REQUIRED_LIBRARIES = {
    'apache_beam': '2.48.0',
    'google.cloud.bigquery': '3.11.0',
    'google.cloud.storage': '2.10.0',
    'pandas': '2.0.0',
    'numpy': '1.24.0',
    'pyarrow': '13.0.0',
    'fastparquet': '2023.10.0'
}

def get_python_version() -> str:
    """Obtiene la versión de Python"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def check_library(library_name: str, min_version: str) -> Tuple[bool, str, str]:
    """
    Verifica si una librería está instalada y su versión
    
    Returns:
        Tuple[bool, str, str]: (instalada, versión_actual, estado)
    """
    try:
        # Intentar importar la librería
        module = importlib.import_module(library_name)
        
        # Obtener versión
        if hasattr(module, '__version__'):
            version = module.__version__
        else:
            version = "Versión no disponible"
        
        # Verificar si cumple con la versión mínima
        if version != "Versión no disponible":
            try:
                from packaging import version as pkg_version
                if pkg_version.parse(version) >= pkg_version.parse(min_version):
                    status = "✅ OK"
                else:
                    status = f"⚠️  Versión {version} < {min_version}"
            except ImportError:
                status = "✅ Instalada (versión no verificada)"
        else:
            status = "✅ Instalada (versión no verificada)"
        
        return True, version, status
        
    except ImportError:
        return False, "No instalada", "❌ No instalada"
    except Exception as e:
        return False, f"Error: {str(e)}", "❌ Error"

def check_gcloud_tools() -> Dict[str, str]:
    """Verifica herramientas de Google Cloud"""
    tools = {}
    
    # Verificar gcloud
    try:
        result = subprocess.run(['gcloud', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            tools['gcloud'] = f"✅ {version_line}"
        else:
            tools['gcloud'] = "❌ No disponible"
    except Exception:
        tools['gcloud'] = "❌ No disponible"
    
    # Verificar bq
    try:
        result = subprocess.run(['bq', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            tools['bq'] = "✅ BigQuery CLI disponible"
        else:
            tools['bq'] = "❌ No disponible"
    except Exception:
        tools['bq'] = "❌ No disponible"
    
    # Verificar gsutil
    try:
        result = subprocess.run(['gsutil', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            tools['gsutil'] = f"✅ {version_line}"
        else:
            tools['gsutil'] = "❌ No disponible"
    except Exception:
        tools['gsutil'] = "❌ No disponible"
    
    return tools

def check_gcp_config() -> Dict[str, str]:
    """Verifica configuración de Google Cloud"""
    config = {}
    
    try:
        # Obtener proyecto actual
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            project = result.stdout.strip()
            config['project'] = f"✅ {project}" if project else "❌ No configurado"
        else:
            config['project'] = "❌ No disponible"
    except Exception:
        config['project'] = "❌ Error"
    
    try:
        # Obtener cuenta actual
        result = subprocess.run(['gcloud', 'config', 'get-value', 'account'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            account = result.stdout.strip()
            config['account'] = f"✅ {account}" if account else "❌ No configurado"
        else:
            config['account'] = "❌ No disponible"
    except Exception:
        config['account'] = "❌ Error"
    
    try:
        # Obtener región actual
        result = subprocess.run(['gcloud', 'config', 'get-value', 'compute/region'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            region = result.stdout.strip()
            config['region'] = f"✅ {region}" if region else "❌ No configurado"
        else:
            config['region'] = "❌ No configurado"
    except Exception:
        config['region'] = "❌ Error"
    
    return config

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICADOR DE LIBRERÍAS Y HERRAMIENTAS")
    print("=" * 60)
    
    # Información del sistema
    print(f"🐍 Python: {get_python_version()}")
    print(f"💻 Sistema: {sys.platform}")
    print()
    
    # Verificar librerías Python
    print("📦 LIBRERÍAS PYTHON REQUERIDAS:")
    print("-" * 40)
    
    all_ok = True
    for lib_name, min_version in REQUIRED_LIBRARIES.items():
        installed, version, status = check_library(lib_name, min_version)
        print(f"{lib_name:<20} {status:<25} {version}")
        if not installed or "❌" in status:
            all_ok = False
    
    print()
    
    # Verificar herramientas de Google Cloud
    print("☁️ HERRAMIENTAS DE GOOGLE CLOUD:")
    print("-" * 40)
    
    gcloud_tools = check_gcloud_tools()
    for tool, status in gcloud_tools.items():
        print(f"{tool:<15} {status}")
        if "❌" in status:
            all_ok = False
    
    print()
    
    # Verificar configuración de GCP
    print("⚙️ CONFIGURACIÓN DE GOOGLE CLOUD:")
    print("-" * 40)
    
    gcp_config = check_gcp_config()
    for config_item, status in gcp_config.items():
        print(f"{config_item:<15} {status}")
        if "❌" in status:
            all_ok = False
    
    print()
    print("=" * 60)
    
    # Resumen final
    if all_ok:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON EXITOSAMENTE!")
        print("✅ Tu entorno está listo para ejecutar el pipeline ultra-rápido")
    else:
        print("⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("🔧 Revisa los elementos marcados con ❌ antes de continuar")
        print("💡 Ejecuta './setup_environment.sh' para configurar el entorno")
    
    print()
    
    # Recomendaciones
    if not all_ok:
        print("📋 RECOMENDACIONES:")
        if any("❌" in status for status in gcloud_tools.values()):
            print("   • Instala Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
        if any("❌" in status for status in gcp_config.values()):
            print("   • Configura tu proyecto: gcloud config set project TU_PROJECT_ID")
            print("   • Autentícate: gcloud auth login")
        if not all_ok:
            print("   • Ejecuta: ./setup_environment.sh")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
