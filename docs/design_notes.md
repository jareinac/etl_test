# Notas de Diseño — ETL Técnico

## Particionado
- Los datos se guardan en formato **Parquet** (columnar, comprimido y eficiente para analítica).
- Se estructuran dos capas:
  - **Raw** → copia fiel de los datos de entrada (JSON).
  - **Curated** → tablas limpias y normalizadas dim_user, dim_product, fact_order.
- En una versión productiva, podría aplicarse **particionado temporal**  para mejorar queries.

## Claves de Identificación
- Cada dimensión y tabla de hechos usa claves únicas:
  - `dim_user`: `user_id`
  - `dim_product`: `product_id`
  - `fact_order`: `order_id`
- Estas claves se usan para garantizar **idempotencia** y consistencia entre ejecuciones.

## Idempotencia
- La función `write_parquet_idempotent` combina datos nuevos con históricos y elimina duplicados por clave.
- Los registros duplicados se guardan en un archivo separado (`*_duplicates.csv`) para auditoría.
- Se generan salidas tanto en **Parquet** como en **CSV**, facilitando compatibilidad y depuración.

## Monitorización y Alertas
- Se registran métricas clave:
  - Número de órdenes procesadas.
  - Cantidad de usuarios únicos y productos cargados.
- Los logs se escriben en:
  - Consola (para ejecución local).
  - Archivo estructurado JSON (`logs/etl_log.json`).
- En producción, estos logs podrían integrarse con otras herramientas.
- Posibles alertas:
  - Ausencia de datos en la ventana esperada.
  - Incremento anómalo de duplicados o errores.
  - Retraso en la ejecución del job.

## Trade-offs
- **Simulación local**: todo corre en disco sin dependencias de nube (más simple, pero menos escalable).
- **Idempotencia con CSV/Parquet**: asegura reproducibilidad, aunque puede ser más lento que usar un motor de metadatos.
- **Logs JSON estructurados**: agregan claridad y monitoreo, pero requieren librerías adicionales o formateadores propios.
- **Duplicados en archivo aparte**: mejora la auditoría, aunque implica espacio extra en almacenamiento.
