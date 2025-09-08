from src.transforms import normalize_orders
import pandas as pd

def test_normalize_and_dedupe():
    raw = [
        {'order_id':'o1','user_id':'u001','created_at':'2025-01-01T00:00:00Z','items':[{'sku':'p_1','qty':1,'price':10}],'amount':10,'currency':'USD'},
        {'order_id':'o2','user_id':'u002','created_at':'2025-02-01T00:00:00Z','items':[{'sku':'p_2','qty':1,'price':10}],'amount':10,'currency':'USD'},
        {'order_id':'o3','user_id':'u003','created_at':'2025-03-01T00:00:00Z','items':[{'sku':'p_3','qty':1,'price':10}],'amount':10,'currency':'USD'},
        {'order_id':'o4','user_id':'u004','created_at':None,'items':[],'amount':5,'currency':'USD'},
        {'order_id':'o3','user_id':'u003','created_at':'2025-03-01T00:00:00Z','items':[{'sku':'p_3','qty':1,'price':10}],'amount':10,'currency':'USD'}
        
    ]
    df = normalize_orders(raw)
    assert df.shape[0] == 4
    assert 'order_id' in df.columns
    assert pd.isna(df.loc[df['order_id']=='o4','created_at']).all()
