#!/usr/bin/env python3
"""
Construção de datasets analíticos Gold
Uso:
  python -m src.etl.load --silver data/silver --gold data/gold
"""
from pathlib import Path
import pandas as pd
from datetime import datetime

SILVER = Path("data/silver")
GOLD = Path("data/gold")

def build_gold(silver_dir=SILVER, gold_dir=GOLD):
    gold_dir.mkdir(parents=True, exist_ok=True)
    # Exemplo: construir indicador por municipio juntando metas e avaliacoes
    metas = pd.concat(list(silver_dir.glob("silver_meta_*.parquet")), axis=0, ignore_index=True) if list(silver_dir.glob("silver_meta_*.parquet")) else pd.DataFrame()
    aval = pd.concat(list(silver_dir.glob("silver_avaliacao_*.parquet")), axis=0, ignore_index=True) if list(silver_dir.glob("silver_avaliacao_*.parquet")) else pd.DataFrame()
    if not metas.empty and not aval.empty:
        # join simplificado por id_municipio, ano, rede, serie
        merged = aval.merge(metas, how="left", left_on=["id_municipio","ano","rede"], right_on=["id_municipio","ano","rede"])
        merged["gap_meta"] = merged["resultado_alfabetizacao"] - merged["meta_alfabetizacao"]
        merged["status_meta"] = merged["gap_meta"].apply(lambda x: "atingiu_meta" if pd.notna(x) and x >= 0 else ("abaixo_meta" if pd.notna(x) else "sem_meta_disponivel"))
        out = gold_dir / "gold_indicador_municipio.parquet"
        merged.to_parquet(out, index=False)
        print(f"Gold built: {out} rows={len(merged)}")
    else:
        print("Insufficient data to build gold datasets")
    return True

if __name__ == "__main__":
    build_gold()
