# Bonus: Visualización en Power BI

## Objetivo
Complementar el pipeline ETL con una capa de visualización que permita a usuarios de negocio explorar los datos transformados y validados.

## Proceso
1. **Carga de datos**  
   - Se conectó Power BI directamente a los archivos **Parquet** generados en la capa *Curated* (`dim_user`, `dim_product`, `fact_order`).  
   - Se validó que los formatos fueran compatibles y reconocidos automáticamente.

2. **Modelado de datos**
   - Se definieron relaciones entre tablas:
     - `dim_user.user_id` ↔ `fact_order.user_id`
     - Se aplicó el modelo **estrella (Star Schema)** para facilitar consultas analíticas.

3. **Datos adicionales**
   - Se agregaron registros de prueba con información **simulada pero realista** de productos y clientes, manteniendo la estructura solicitada, para enriquecer el análisis.

4. **Visualizaciones creadas**
   - **Panel de órdenes**: volumen de órdenes por fecha y usuario.  
   - **Top productos**: ranking de ventas por producto.  
   - **Usuarios activos**: métricas de clientes recurrentes vs nuevos.  
   - **Calidad de datos**: duplicados detectados vs registros únicos.

5. **Validación**
   - Se contrastaron los conteos de Power BI con las métricas del log estructurado (`etl_log.json`) para confirmar consistencia.

## Pantallazos
- [ ] Diagrama de modelo en Power BI (relaciones entre tablas).  
- [ ] Reporte de órdenes y usuarios.  
- [ ] Panel de calidad de datos.

## Conclusión
La integración con Power BI permite a usuarios finales visualizar los datos procesados sin depender del pipeline técnico. Esto demuestra cómo el ETL puede **alimentar directamente dashboards de negocio** y facilitar la toma de decisiones.
