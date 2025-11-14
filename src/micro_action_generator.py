import random

# -------------------------------------------------------------------
# Safe, empathetic micro-actions for each mood category
# -------------------------------------------------------------------
SAFE_ACTIONS = {
    "anxious": [
        "Take a short deep breathing break",
        "Go for a 10-minute walk outdoors",
        "Write down one thing you're grateful for"
    ],
    "sad": [
        "Reach out to a friend or family member",
        "Listen to uplifting music",
        "Do a small act of kindness"
    ],
    "happy": [
        "Reflect on what made today positive",
        "Capture your good mood in a journal",
        "Encourage someone else with positivity"
    ],
    "calm": [
        "Maintain your evening relaxation routine",
        "Spend a few minutes in mindful silence",
        "Enjoy a quiet tea or light reading"
    ],
    "neutral": [
        "Take a short mindful pause during your day",
        "Stretch gently for 5 minutes",
        "Spend a moment appreciating your surroundings"
    ]
}

# -------------------------------------------------------------------
# Generate safe, contextual micro-actions based on the pattern
# -------------------------------------------------------------------
def generate_micro_actions(pattern_description: str):
    """
    Generates 3 short, empathetic micro-actions for the given mood pattern.
    """
    key = next((m for m in SAFE_ACTIONS if m in pattern_description.lower()), "calm")
    actions = random.sample(SAFE_ACTIONS[key], 3)
    return append_safety_note(actions, pattern_description)

# -------------------------------------------------------------------
# Append a safety fallback when recurring distress signals appear
# -------------------------------------------------------------------
def append_safety_note(actions, pattern_description):
    """
    Adds a safe fallback message if the pattern indicates persistent distress.
    """
    distress_keywords = ["sad", "anxious", "stress", "depressed", "lonely"]
    if any(word in pattern_description.lower() for word in distress_keywords):
        actions.append(
            "If these feelings persist, consider reaching out to a trusted friend or mental health professional."
        )
    return actions
