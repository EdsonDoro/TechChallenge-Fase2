#!/usr/bin/env python3
"""
Ingestão batch: lê CSVs em data/raw e grava Parquet em data/bronze
Uso:
  python -m src.etl.ingest --input data/raw --output data/bronze --pattern "*.csv"
"""
from pathlib import Path
import pandas as pd
from datetime import datetime
import argparse
import pyarrow as pa

def ingest_file(src: Path, dst: Path, sep=",", encoding="utf-8"):
    df = pd.read_csv(src, sep=sep, encoding=encoding, low_memory=False)
    df["_data_ingestao"] = datetime.utcnow().isoformat()
    df["_origem"] = str(src.name)
    dst.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(dst, index=False)
    return len(df)

def main(input_dir, output_dir, pattern):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    files = list(input_dir.rglob(pattern))
    summary = {}
    for f in files:
        out = output_dir / f.with_suffix(".parquet").name
        rows = ingest_file(f, out, sep=";" if str(f).lower().endswith(".csv") and "microdados" in str(f).lower() else ",")
        summary[str(f)] = {"rows": rows, "output": str(out)}
        print(f"Ingested {f} -> {out} ({rows} rows)")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw")
    parser.add_argument("--output", default="data/bronze")
    parser.add_argument("--pattern", default="*.csv")
    args = parser.parse_args()
    main(args.input, args.output, args.pattern)
