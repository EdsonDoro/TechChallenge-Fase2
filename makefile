.PHONY: ingest transform load stream-consume stream-simulate dq test

ingest:
    python -m src.etl.ingest --input data/raw --output data/bronze

transform:
    python -m src.etl.transform

load:
    python -m src.etl.load

stream-simulate:
    python -m src.stream.simulate --n 50

stream-consume:
    python -m src.stream.consumer

dq:
    python -c "from src.dq.checks import run_all_checks; print('run dq')"

test:
    pytest -q
