MOOD_SCORES = {
    "happy": 5,
    "calm": 4,
    "neutral": 3,
    "sad": 2,
    "anxious": 1
}

def map_mood_to_score(mood: str) -> int:
    return MOOD_SCORES.get(mood.lower(), 3)
