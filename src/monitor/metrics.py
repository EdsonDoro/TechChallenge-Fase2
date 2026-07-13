#!/usr/bin/env python3
"""
Emite métricas simples em JSON para integração com observability
"""
import json
from datetime import datetime
from pathlib import Path

OUT = Path("data/metrics")
OUT.mkdir(parents=True, exist_ok=True)

def emit(metric_name, value, tags=None):
    payload = {
        "metric": metric_name,
        "value": value,
        "tags": tags or {},
        "ts": datetime.utcnow().isoformat()
    }
    path = OUT / f"{metric_name}_{int(datetime.utcnow().timestamp())}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False))
    print("Emitted", path)
    return path
