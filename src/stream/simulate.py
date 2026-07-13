#!/usr/bin/env python3
"""
Simulador de eventos streaming que grava JSONs em data/raw/stream_events
Uso:
  python -m src.stream.simulate --n 100
"""
from faker import Faker
from pathlib import Path
import json
import argparse
import random
from datetime import datetime

OUT = Path("data/raw/stream_events")
OUT.mkdir(parents=True, exist_ok=True)
fake = Faker("pt_BR")

def gen_event():
    return {
        "tipo_evento": "atualizacao_indicador",
        "ano": random.choice([2024,2025]),
        "id_municipio": str(random.randint(1100000, 5300000)).zfill(7),
        "rede": random.choice(["municipal","estadual"]),
        "serie": random.choice(["2EF","3EF"]),
        "resultado_alfabetizacao": round(random.uniform(20, 100), 2),
        "data_evento": datetime.utcnow().isoformat()
    }

def main(n):
    for i in range(n):
        ev = gen_event()
        path = OUT / f"event_{i}_{int(datetime.utcnow().timestamp())}.json"
        path.write_text(json.dumps(ev, ensure_ascii=False))
        print("Wrote", path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10)
    args = parser.parse_args()
    main(args.n)
