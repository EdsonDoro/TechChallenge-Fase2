#!/usr/bin/env python3
"""
Regras de Data Quality e exportação de quarentena
"""
import pandas as pd

def check_percentual_range(df, col):
    invalid = df[(df[col].notna()) & ((df[col] < 0) | (df[col] > 100))]
    return invalid

def check_duplicates(df, subset):
    dup = df[df.duplicated(subset=subset, keep=False)]
    return dup

def run_all_checks(df):
    results = {}
    if "resultado_alfabetizacao" in df.columns:
        results["percentual_invalid"] = check_percentual_range(df, "resultado_alfabetizacao")
    # add more checks as needed
    return results
