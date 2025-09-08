from typing import List, Dict, Any
import pandas as pd

def normalize_orders(raw_orders: List[Dict[str, Any]]):
    rows = []
    for o in raw_orders:
        if not o.get('order_id') or not o.get('user_id'):
            continue
        ca = o.get('created_at')
        try:
            dt = pd.to_datetime(ca, utc=True) if ca else pd.NaT
        except Exception:
            dt = pd.NaT
        items = o.get('items') or []
        total_qty = sum((it.get('qty') or 0) for it in items)
        rows.append({
            'order_id': o.get('order_id'),
            'user_id': o.get('user_id'),
            'amount': o.get('amount'),
            'currency': o.get('currency'),
            'created_at': dt,
            'total_qty': total_qty,
            'raw': o
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = df.drop_duplicates(subset=['order_id'], keep='first').reset_index(drop=True)
    return df

def build_dim_user(users_csv_path: str):
    df = pd.read_csv(users_csv_path, parse_dates=['created_at'])
    return df

def build_dim_product(products_csv_path: str):
    df = pd.read_csv(products_csv_path)
    return df

def build_fact_order(orders_df):
    df = orders_df.copy()
    if 'created_at' in df:
        df['created_date'] = df['created_at'].dt.date
    else:
        df['created_date'] = None
    fact = df[['order_id','user_id','amount','currency','created_at','total_qty','created_date']]
    return fact
