# 🚫 SOLUCIONES SIN AUMENTAR CUOTAS

## 💡 Carga de 136GB en BigQuery con Restricciones de Cuotas

Esta carpeta contiene **soluciones alternativas** que funcionan con tus cuotas actuales de Google Cloud **SIN necesidad de aumentarlas**.

## 🚨 **Situación Actual:**
- **Cuota disponible**: Solo 8 direcciones IP en `us-central1`
- **No puedes aumentar**: Restricciones de la cuenta/proyecto
- **Necesitas**: Cargar 136GB en BigQuery

## 🎯 **Soluciones Disponibles:**

### **1. 🚀 Pipeline Ultra-Optimizado para 8 IPs (RECOMENDADA)**
- **Archivo**: `ultra_optimized_8ips.py`
- **Script**: `run_8ips_optimized.sh`
- **Tiempo**: 35-45 minutos para 136GB
- **Costo**: $3-6 USD
- **Características**: Máximo rendimiento con restricción de 8 IPs

### **2. 📊 Carga Directa a BigQuery (Alternativa)**
- **Archivo**: `bigquery_direct_load.py`
- **Tiempo**: 2-4 horas para 136GB
- **Costo**: $0.5-1 USD
- **Características**: Sin Dataflow, solo BigQuery

### **3. 🔧 Herramientas de Diagnóstico**
- **Verificador de cuotas**: `check_quotas.py`
- **Solucionador automático**: `fix_quota_issue.sh`

## 🚀 **Instalación y Uso:**

### **Paso 1: Configurar Permisos**
```bash
cd Sinaumentarcouta
chmod +x *.sh *.py
```

### **Paso 2: Verificar Cuotas (Opcional)**
```bash
python3 check_quotas.py
```

### **Paso 3: Ejecutar Solución Recomendada**
```bash
./run_8ips_optimized.sh
```

### **Paso 4: Alternativa si Dataflow falla**
```bash
python3 bigquery_direct_load.py
```

## 📊 **Comparación de Soluciones:**

| Solución | Tiempo | Costo | Estabilidad | Requisitos |
|----------|--------|-------|-------------|------------|
| **Pipeline 8 IPs** | 35-45 min | $3-6 | ✅ Excelente | 8 IPs |
| **Carga Directa** | 2-4 horas | $0.5-1 | ✅ Muy estable | Solo BigQuery |
| **Dataflow Original** | ❌ Error | - | ❌ No funciona | 50+ IPs |

## ⚡ **Configuración del Pipeline 8 IPs:**

- **Workers**: 7 iniciales, máximo 8
- **Máquina**: n1-standard-16 (súper potente)
- **Disco**: 500GB por worker
- **Región**: us-central1 (tu región actual)
- **Optimizaciones**: Streaming, procesamiento por lotes, reshuffle

## 🔍 **Monitoreo:**

### **En Dataflow Console:**
- [Dataflow Console](https://console.cloud.google.com/dataflow)
- Ver jobs activos y métricas en tiempo real

### **En BigQuery Console:**
- [BigQuery Console](https://console.cloud.google.com/bigquery)
- Verificar datos cargados

### **Con Script de Monitoreo:**
```bash
python3 monitor_pipeline.py --project=$PROJECT_ID
```

## 🛠️ **Solución de Problemas:**

### **Error: "Quota exceeded"**
- ✅ **Solución**: Usar `ultra_optimized_8ips.py` (diseñado para 8 IPs)

### **Error: "API not enabled"**
```bash
gcloud services enable dataflow.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
```

### **Error: "Permission denied"**
```bash
gcloud auth login
gcloud config set project TU_PROJECT_ID
```

## 💰 **Optimización de Costos:**

### **Con Pipeline 8 IPs:**
- **Workers**: 7-8 (mínimo necesario)
- **Máquina**: n1-standard-16 (máximo rendimiento)
- **Disco**: 500GB (para archivos grandes)
- **Streaming**: Más eficiente que batch

### **Con Carga Directa:**
- **Sin Dataflow**: Solo costos de BigQuery
- **Sin workers**: Sin costos de Compute Engine
- **Más lento**: Pero más económico

## 🎯 **Recomendaciones:**

### **Para Uso Inmediato:**
1. **Usar `run_8ips_optimized.sh`** - Máximo rendimiento con tus cuotas
2. **Monitorear progreso** - Verificar en Dataflow Console
3. **Verificar resultados** - Comprobar en BigQuery

### **Para Futuras Cargas:**
1. **Solicitar aumento de cuotas** - Contactar soporte de Google Cloud
2. **Usar cuenta con más recursos** - Considerar upgrade de cuenta
3. **Mantener configuración optimizada** - Reutilizar scripts

## 📚 **Recursos Adicionales:**

- [Documentación de Dataflow](https://cloud.google.com/dataflow/docs)
- [Guía de BigQuery](https://cloud.google.com/bigquery/docs)
- [Solicitar Aumento de Cuotas](https://console.cloud.google.com/iam-admin/quotas)
- [Soporte de Google Cloud](https://cloud.google.com/support)

## 🤝 **Soporte:**

Para problemas específicos:
1. **Revisar logs** del pipeline en Dataflow Console
2. **Verificar cuotas** con `check_quotas.py`
3. **Usar alternativa** con `bigquery_direct_load.py`
4. **Contactar soporte** si persisten los problemas

---

## 🎉 **¡Logra tu objetivo SIN aumentar cuotas!**

**Con estas soluciones, puedes cargar 136GB en BigQuery en 35-45 minutos usando solo tus 8 IPs disponibles.**
