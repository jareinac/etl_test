import time, json, random
from pathlib import Path

def fetch_orders_mock(path: str):
    """Simulate API fetch with simple retry logic reading local file."""
    max_retries = 3
    for attempt in range(1, max_retries+1):
        try:
            # simulate transient failure
            if random.random() < 0.05:
                raise RuntimeError('Transient API error')
            p = Path(path)
            return json.loads(p.read_text())
        except Exception as e:
            if attempt == max_retries:
                raise
            time.sleep(0.5 * attempt)
    return []
