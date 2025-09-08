import argparse
import json
from pathlib import Path
import pandas as pd

from src.api_client import fetch_orders_mock
from src.transforms import normalize_orders, build_dim_user, build_dim_product, build_fact_order
from src.db import write_parquet_idempotent
from src.logging_utils import log_metric, log_event
from src.logger_config import get_logger


def main(sample_dir, output_dir, since=None):
    sample_dir = Path(sample_dir)
    output_dir = Path(output_dir)
    output_raw = output_dir / 'raw'
    output_curated = output_dir / 'curated'

    output_raw.mkdir(parents=True, exist_ok=True)
    output_curated.mkdir(parents=True, exist_ok=True)

    logger = get_logger()
    log_event(logger, "ETL Job", "START")
    
    # 1. Extraer datos desde el mock
    orders = fetch_orders_mock(str(sample_dir / 'api_orders.json'))

    # 2. Guardar copia en RAW
    (output_raw / 'api_orders.json').write_text(json.dumps(orders, indent=2))

    # 3. Normalizar pedidos
    orders_df = normalize_orders(orders)
    if since:
        orders_df = orders_df[orders_df['created_at'] >= pd.to_datetime(since, utc=True)]

    # 4. Construir dimensiones y hechos
    dim_user = build_dim_user(str(sample_dir / 'users.csv'))
    log_metric(logger,"dim_user", "records", len(dim_user))

    dim_product = build_dim_product(str(sample_dir / 'products.csv'))
    log_metric(logger,"dim_product", "records", len(dim_product))

    fact_order = build_fact_order(orders_df)
    log_metric(logger,"fact_order", "records", len(fact_order))

    # 5. Guardar outputs en curated
    write_parquet_idempotent(dim_user, str(output_curated / 'dim_user.parquet'), subset_keys=['user_id'])
    write_parquet_idempotent(dim_product, str(output_curated / 'dim_product.parquet'), subset_keys=['product_id'])
    write_parquet_idempotent(fact_order, str(output_curated / 'fact_order.parquet'), subset_keys=['order_id'])
    print('✅ ETL finished. Outputs in', output_dir)
    logger.info("ETL finished", extra={"step": "end", "output_dir": str(output_dir)})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample-dir', default='../sample_data')
    parser.add_argument('--output-dir', default='../output')
    parser.add_argument('--since', default=None)
    args = parser.parse_args()

    main(args.sample_dir, args.output_dir, args.since)
