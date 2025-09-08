# Prueba Técnica — Data Engineer (ETL Pipeline)

##  Descripción
Este proyecto implementa un **pipeline ETL reproducible en Python**, tomando datos de entrada en formato **JSON/CSV**, aplicando transformaciones y generando salidas en **Parquet y CSV**.  
El objetivo es evaluar la capacidad de construir un flujo de datos idempotente, modular, probado y documentado.



# ETL Test 
Stack: Python (pandas), Parquet outputs, logging.

## Reproducir localmente
1. Crear y activar virtualenv:
   python -m venv venv
2. Instalar dependencias:
   pip install -r requirements.txt
3. Ejecutar job:
   python -m src.etl_job --sample-dir sample_data --output-dir output
   (para ejecución incremental): add `--since 2025-09-01T00:00:00Z`
4. Correr tests:
   pytest -q

Output esperado :
- output/raw/api_orders.json
- output/curated/dim_user.parquet
- output/curated/dim_product.parquet
- output/curated/fact_order.parquet
- output/curated/dim_user.cvs
- output/curated/dim_product.cvs
- output/curated/fact_order.cvs
- output/curated/dim_user_duplicates.cvs
- output/curated/dim_product_duplicates.cvs
- output/curated/fact_order_duplicates.cvs
- logs/etl_log.json


# Monitorización y Alertas

- Logs estructurados en JSON guardados en logs/etl_log.json.
- Métricas registradas: volumen de órdenes procesadas, usuarios y productos únicos.
- Alertas planteadas (en entorno real): ausencia de datos, anomalías en volumen, errores repetitivos, tiempos de ejecución elevados.

# Tiempo estimado de implementación: 16 horas.
