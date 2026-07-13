import pandas as pd
from src.dq.checks import check_percentual_range

def test_check_percentual_range():
    df = pd.DataFrame({"resultado_alfabetizacao": [50, -1, 120, None]})
    invalid = check_percentual_range(df, "resultado_alfabetizacao")
    assert len(invalid) == 2
