# FinOps - Estimativa e otimizações

## Premissas
- Volume de dados bruto: 50 GB
- Armazenamento Parquet (compressão): 50 GB -> 15 GB efetivos
- Consultas analíticas esporádicas (BigQuery/Athena): 100 consultas/mês

## Estimativa simplificada (exemplo AWS)
- S3 Standard (15 GB): ~ $0.36 / mês
- Glue / small compute (10 horas/mês): ~ $2.00 / mês
- Athena queries (100 queries, 1 GB scanned avg): ~ $5.00 / mês
- Total estimado: ~ $7-10 / mês

## Otimizações aplicadas
- Uso de Parquet e compressão
- Particionamento por `ano` e `sigla_uf`
- Jobs sob demanda (evitar clusters permanentes)
- Ciclo de vida para mover dados frios para armazenamento mais barato
