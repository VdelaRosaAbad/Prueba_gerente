#!/usr/bin/env python3
"""
🔍 Verificador de Cuotas de Google Cloud
📊 Muestra cuotas disponibles en diferentes regiones
🚨 Identifica limitaciones que pueden afectar Dataflow
"""

import subprocess
import json
import sys
from typing import Dict, List, Tuple

def run_gcloud_command(command: str) -> str:
    """Ejecuta comando de gcloud y retorna el resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_project_info() -> Dict[str, str]:
    """Obtiene información del proyecto actual"""
    project_id = run_gcloud_command("gcloud config get-value project")
    account = run_gcloud_command("gcloud config get-value account")
    
    return {
        "project_id": project_id,
        "account": account
    }

def check_region_quotas(region: str, project_id: str) -> Dict[str, any]:
    """Verifica cuotas en una región específica"""
    print(f"🔍 Verificando cuotas en región: {region}")
    
    # Comando para obtener todas las cuotas de la región
    command = f"gcloud compute regions describe {region} --project={project_id} --format=json"
    result = run_gcloud_command(command)
    
    if result.startswith("Error:"):
        return {"error": result}
    
    try:
        region_data = json.loads(result)
        quotas = region_data.get('quotas', [])
        
        quota_info = {}
        for quota in quotas:
            metric = quota.get('metric', '')
            limit = quota.get('limit', 0)
            usage = quota.get('usage', 0)
            
            quota_info[metric] = {
                "limit": limit,
                "usage": usage,
                "available": limit - usage if limit and usage else "N/A"
            }
        
        return quota_info
        
    except json.JSONDecodeError:
        return {"error": "Error decodificando JSON de la región"}

def get_recommended_regions() -> List[str]:
    """Retorna lista de regiones recomendadas para Dataflow"""
    return [
        "us-east1",      # Estados Unidos Este (generalmente mejores cuotas)
        "us-west1",      # Estados Unidos Oeste
        "europe-west1",  # Europa Occidental
        "asia-southeast1", # Asia Sudeste
        "us-central1",   # Estados Unidos Central (tu región actual)
        "europe-west4",  # Europa Occidental 4
        "us-east4"       # Estados Unidos Este 4
    ]

def analyze_quotas_for_dataflow(quotas: Dict[str, any]) -> Dict[str, any]:
    """Analiza cuotas específicamente para Dataflow"""
    analysis = {
        "dataflow_ready": False,
        "recommendations": [],
        "critical_issues": [],
        "warnings": []
    }
    
    # Verificar cuotas críticas para Dataflow
    critical_quotas = {
        "IN_USE_ADDRESSES": "Direcciones IP en uso",
        "CPUS": "CPUs",
        "DISKS_TOTAL_GB": "Disco total",
        "INSTANCES": "Instancias"
    }
    
    for quota_name, description in critical_quotas.items():
        if quota_name in quotas:
            quota_data = quotas[quota_name]
            limit = quota_data.get("limit", 0)
            usage = quota_data.get("usage", 0)
            
            if quota_name == "IN_USE_ADDRESSES":
                if limit < 20:
                    analysis["critical_issues"].append(
                        f"❌ {description}: Límite muy bajo ({limit}). Necesitas al menos 20 para Dataflow eficiente."
                    )
                elif limit < 50:
                    analysis["warnings"].append(
                        f"⚠️  {description}: Límite moderado ({limit}). Dataflow funcionará pero con rendimiento limitado."
                    )
                else:
                    analysis["recommendations"].append(
                        f"✅ {description}: Límite adecuado ({limit}) para Dataflow eficiente."
                    )
            
            elif quota_name == "CPUS":
                if limit < 32:
                    analysis["warnings"].append(
                        f"⚠️  {description}: Límite de CPU moderado ({limit}). Considera usar máquinas más potentes."
                    )
                else:
                    analysis["recommendations"].append(
                        f"✅ {description}: Límite de CPU adecuado ({limit})."
                    )
    
    # Determinar si la región está lista para Dataflow
    if not analysis["critical_issues"]:
        analysis["dataflow_ready"] = True
    
    return analysis

def main():
    """Función principal"""
    print("🔍 VERIFICADOR DE CUOTAS PARA DATAFLOW")
    print("=" * 60)
    
    # Obtener información del proyecto
    project_info = get_project_info()
    project_id = project_info["project_id"]
    account = project_info["account"]
    
    if project_id.startswith("Error:"):
        print(f"❌ Error obteniendo proyecto: {project_id}")
        return 1
    
    print(f"📊 Proyecto: {project_id}")
    print(f"👤 Cuenta: {account}")
    print()
    
    # Verificar cuotas en regiones recomendadas
    recommended_regions = get_recommended_regions()
    
    best_region = None
    best_score = 0
    
    for region in recommended_regions:
        print(f"🌍 Verificando región: {region}")
        print("-" * 40)
        
        quotas = check_region_quotas(region, project_id)
        
        if "error" in quotas:
            print(f"❌ Error: {quotas['error']}")
            print()
            continue
        
        # Analizar cuotas para Dataflow
        analysis = analyze_quotas_for_dataflow(quotas)
        
        # Mostrar análisis
        if analysis["critical_issues"]:
            print("🚨 PROBLEMAS CRÍTICOS:")
            for issue in analysis["critical_issues"]:
                print(f"   {issue}")
        
        if analysis["warnings"]:
            print("⚠️  ADVERTENCIAS:")
            for warning in analysis["warnings"]:
                print(f"   {warning}")
        
        if analysis["recommendations"]:
            print("✅ RECOMENDACIONES:")
            for rec in analysis["recommendations"]:
                print(f"   {rec}")
        
        # Calcular score de la región
        score = 0
        if analysis["dataflow_ready"]:
            score += 10
        score += len(analysis["recommendations"]) * 2
        score -= len(analysis["warnings"])
        score -= len(analysis["critical_issues"]) * 5
        
        print(f"📊 Score de región: {score}/10")
        
        # Actualizar mejor región
        if score > best_score:
            best_score = score
            best_region = region
        
        print()
    
    # Resumen final
    print("=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    if best_region:
        print(f"🏆 MEJOR REGIÓN: {best_region} (Score: {best_score}/10)")
        print()
        
        if best_score >= 8:
            print("🎉 ¡Excelente! Esta región está perfectamente configurada para Dataflow.")
        elif best_score >= 6:
            print("✅ Buena opción. Dataflow funcionará bien con algunas limitaciones menores.")
        elif best_score >= 4:
            print("⚠️  Región aceptable. Dataflow funcionará pero con rendimiento limitado.")
        else:
            print("❌ Región problemática. Considera solicitar aumento de cuotas.")
        
        print()
        print("🚀 PRÓXIMOS PASOS:")
        print(f"1. Configurar región: gcloud config set compute/region {best_region}")
        print(f"2. Configurar Dataflow: gcloud config set dataflow/region {best_region}")
        print("3. Ejecutar: ./fix_quota_issue.sh")
        print("4. O usar: python3 quota_optimized_loader.py")
        
    else:
        print("❌ No se encontró ninguna región adecuada para Dataflow.")
        print("🔧 Considera:")
        print("   • Solicitar aumento de cuotas en Google Cloud")
        print("   • Usar una cuenta con más recursos")
        print("   • Contactar soporte de Google Cloud")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
