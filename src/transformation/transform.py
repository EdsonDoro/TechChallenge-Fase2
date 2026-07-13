#!/usr/bin/env python3
"""
Transformações e validações para camada Silver
Uso:
  python -m src.etl.transform --bronze data/bronze --silver data/silver
"""
from pathlib import Path
import pandas as pd
from datetime import datetime
import unicodedata
import re
import json

BRONZE = Path("data/bronze")
SILVER = Path("data/silver")
QUARANTINE = SILVER / "quarantine"

def normalizar_nome_coluna(col):
    col = col.strip().lower()
    col = unicodedata.normalize("NFKD", col).encode("ascii", errors="ignore").decode("utf-8")
    col = re.sub(r"[^\w]+", "_", col)
    col = re.sub(r"_+", "_", col).strip("_")
    return col

def padronizar_colunas(df):
    df = df.copy()
    df.columns = [normalizar_nome_coluna(c) for c in df.columns]
    return df

def padronizar_campos_comuns(df):
    df = df.copy()
    if "ano" in df.columns:
        df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    if "sigla_uf" in df.columns:
        df["sigla_uf"] = df["sigla_uf"].astype(str).str.strip().str.upper().replace({"NAN": None, "NONE": None})
    if "id_municipio" in df.columns:
        df["id_municipio"] = df["id_municipio"].astype(str).str.replace(".0", "", regex=False).str.zfill(7)
    for col in df.columns:
        if any(k in col for k in ["percentual", "meta", "taxa", "indicador", "resultado"]):
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["_data_processamento"] = datetime.utcnow().isoformat()
    df["_camada_origem"] = "bronze"
    return df

def separar_validos_invalidos(df, required_keys):
    df = df.copy()
    invalid = pd.Series(False, index=df.index)
    for k in required_keys:
        if k in df.columns:
            invalid = invalid | df[k].isna()
    if "ano" in df.columns:
        invalid = invalid | ~df["ano"].between(2020, 2030)
    valid_df = df[~invalid].reset_index(drop=True)
    invalid_df = df[invalid].reset_index(drop=True)
    return valid_df, invalid_df

def process_all(bronze_dir=BRONZE, silver_dir=SILVER):
    silver_dir.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    for p in bronze_dir.glob("*.parquet"):
        df = pd.read_parquet(p)
        df = padronizar_colunas(df)
        df = padronizar_campos_comuns(df)
        required = ["ano", "sigla_uf"] if "sigla_uf" in df.columns else ["ano", "id_municipio"]
        valid, invalid = separar_validos_invalidos(df, required)
        out = silver_dir / f"silver_{p.name}"
        valid.to_parquet(out, index=False)
        if not invalid.empty:
            invalid.to_parquet(QUARANTINE / f"quarantine_{p.name}", index=False)
        print(f"Processed {p.name}: valid={len(valid)} invalid={len(invalid)} -> {out}")
    return True

if __name__ == "__main__":
    process_all()
