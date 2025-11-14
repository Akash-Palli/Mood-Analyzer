import pandas as pd
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from sentence_transformers import SentenceTransformer

# Initialize the model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def detect_temporal_patterns(df: pd.DataFrame):
    patterns = []
    # Weekday-based analysis
    df["weekday"] = df["date"].dt.day_name()
    mean_by_day = df.groupby("weekday")["mood_score"].mean().sort_values()
    
    # Calculate overall average for comparison
    overall_mean = df["mood_score"].mean()
    
    # ---- Low Day Pattern ----
    low_day_name = mean_by_day.index[0]
    low_day_mean = mean_by_day.iloc[0]
    
    if low_day_mean < overall_mean - 0.5: # Only if significantly lower
        # Temporal patterns are based only on rule evidence, use a rule-based confidence
        confidence = compute_confidence([], len(df[df["weekday"] == low_day_name]))
        
        patterns.append({
            "description": f"Mood dips on {low_day_name}s",
            "evidence": df[df["weekday"] == low_day_name][["date", "mood"]].to_dict(orient="records"),
            "confidence": confidence
        })
        
    # ---- High Day Pattern ----
    high_day_name = mean_by_day.index[-1]
    high_day_mean = mean_by_day.iloc[-1]
    
    if high_day_mean > overall_mean + 0.5: # Only if significantly higher
        confidence = compute_confidence([], len(df[df["weekday"] == high_day_name]))
        
        patterns.append({
            "description": f"Mood peaks on {high_day_name}s",
            "evidence": df[df["weekday"] == high_day_name][["date", "mood"]].to_dict(orient="records"),
            "confidence": confidence
        })
        
    return patterns

def cluster_note_patterns(df: pd.DataFrame, model=model):
    """
    Cluster similar notes using sentence embeddings, returning detected patterns.
    The evidence now includes the 'cluster' ID.
    """
    if "notes" not in df.columns or df["notes"].isna().all():
        return []

    # ---- 1️⃣ Encode notes & KMeans clustering ----
    notes = df["notes"].fillna("").tolist()
    embeddings = model.encode(notes)

    # Ensure n_clusters is not greater than the number of data points
    n_clusters = min(3, len(df))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    df["cluster"] = kmeans.fit_predict(embeddings)

    # ---- 2️⃣ Summarize each cluster ----
    cluster_summaries = []
    for cid in df["cluster"].unique():
        subset = df[df["cluster"] == cid].copy()

        # dominant mood
        top_mood = Counter(subset["mood"]).most_common(1)[0][0]

        # intra-cluster distances (tightness)
        cluster_embeddings = embeddings[df["cluster"] == cid]
        distances = pairwise_distances(cluster_embeddings)
        # Handle case of single point cluster
        avg_distance = np.mean(distances[np.triu_indices_from(distances, k=1)]) if len(subset) > 1 else 0

        # confidence score
        confidence = compute_confidence([avg_distance], len(subset))

        # ---- assemble summary (INCLUDES 'cluster' IN EVIDENCE) ----
        # Temporarily create a column for the cluster ID to include it in the dict output
        subset.loc[:, 'cluster'] = cid
        cluster_summaries.append({
            "description": f"Cluster {cid} shows frequent '{top_mood}' moods",
            "evidence": subset[["date", "mood", "notes", "cluster"]].to_dict(orient="records"),
            "confidence": confidence
        })

    return cluster_summaries


def compute_confidence(cluster_distances, evidence_count):
    """
    Compute confidence score for detected pattern.
    - cluster_distances: list of pairwise distances within cluster (or empty list for temporal rules)
    - evidence_count: number of data points supporting the pattern
    Returns float between 0 and 1.
    """
    if not cluster_distances or np.isnan(cluster_distances).all():
        cluster_score = 0.5  # neutral baseline for temporal or single-point rules
    else:
        # Tighter clusters (lower distance) = higher score
        mean_dist = np.mean(cluster_distances)
        # Using softplus-like curve for better normalization
        cluster_score = 1 / (1 + np.exp(mean_dist - 0.7)) 

    # Normalize evidence-based factor (max 5 supporting points = strong pattern)
    rule_score = min(evidence_count / 5, 1.0)

    # Weighted combination
    confidence = (0.6 * cluster_score) + (0.4 * rule_score)
    return round(float(confidence), 2)