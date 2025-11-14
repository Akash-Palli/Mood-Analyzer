import pandas as pd
from src.pattern_detector import detect_temporal_patterns

def test_detect_temporal_patterns():
    data = [
        {"date": "2025-10-25", "mood": "sad"},
        {"date": "2025-10-26", "mood": "happy"}
    ]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["mood_score"] = [2, 5]
    patterns = detect_temporal_patterns(df)
    assert isinstance(patterns, list)
    assert "description" in patterns[0]
