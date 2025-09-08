from pathlib import Path
import pandas as pd


def write_parquet_idempotent(df: pd.DataFrame, out_path: str, subset_keys: list[str] = None):
    """
    Guarda un DataFrame en parquet y csv de manera idempotente.
    Los duplicados se guardan en un archivo separado *_duplicates.csv.
    """
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    subset_keys = subset_keys or []

    try:
        if p.exists():
            existing = pd.read_parquet(p)
            combined = pd.concat([existing, df], ignore_index=True)
        else:
            combined = df

        # deduplicación por claves válidas
        valid_keys = [k for k in subset_keys if k in combined.columns]
        if valid_keys:
            duplicates = combined[combined.duplicated(subset=valid_keys, keep="first")]
            if not duplicates.empty:
                dup_path = p.with_name(p.stem + "_duplicates.csv")
                duplicates.to_csv(dup_path, mode="a", header=not dup_path.exists(), index=False)
            combined = combined.drop_duplicates(subset=valid_keys, keep="last")

        combined.to_parquet(p, index=False)
        csv_path = p.with_suffix(".csv")
        combined.to_csv(csv_path, index=False)

    except Exception:
        # fallback csv
        csv_path = p.with_suffix('.csv')
        if csv_path.exists():
            existing = pd.read_csv(csv_path)
            combined = pd.concat([existing, df], ignore_index=True)
        else:
            combined = df

        valid_keys = [k for k in subset_keys if k in combined.columns]
        if valid_keys:
            duplicates = combined[combined.duplicated(subset=valid_keys, keep="first")]
            if not duplicates.empty:
                dup_path = csv_path.with_name(csv_path.stem + "_duplicates.csv")
                duplicates.to_csv(dup_path, mode="a", header=not dup_path.exists(), index=False)
            combined = combined.drop_duplicates(subset=valid_keys, keep="last")

        combined.to_csv(csv_path, index=False)
    
  
