#!/usr/bin/env python3
"""
Consumer simples que aplica upsert incremental dos eventos na Silver/Gold
Uso:
  python -m src.stream.consumer
"""
from pathlib import Path
import json
import pandas as pd

EVENTS = Path("data/raw/stream_events")
SILVER = Path("data/silver")
GOLD = Path("data/gold")

def consume_all():
    files = sorted(EVENTS.glob("*.json"))
    for f in files:
        ev = json.loads(f.read_text())
        # exemplo: append ao silver de eventos
        df_ev = pd.DataFrame([ev])
        df_ev.to_parquet(SILVER / f"silver_stream_{f.stem}.parquet", index=False)
        print("Consumed", f)
        f.unlink()
    # opcional: chamar load.build_gold() para reprocessar gold incremental
    return True

if __name__ == "__main__":
    consume_all()
