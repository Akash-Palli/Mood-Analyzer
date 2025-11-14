import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from adjustText import adjust_text

# Define colors for clusters for visual differentiation
# These colors will be used cyclically for Cluster 0, Cluster 1, Cluster 2, etc.
CLUSTER_COLORS = ['#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6'] # Red, Green, Blue, Orange, Purple, Cyan, Magenta

def plot_mood_trend(df, output_path="outputs/mood_trend.png", rolling_window=3, annotate_patterns=None):
    """
    Generate an intelligent, publication-quality mood trend plot with auto-adjusted annotations.
    Annotations display the mood word near the relevant point, and cluster points are distinctly colored.

    Args:
        df (pd.DataFrame): Must include 'date', 'mood', and 'mood_score'
        output_path (str): Path to save PNG
        rolling_window (int): Rolling average window
        annotate_patterns (list): Optional detected patterns
    """
    # Use a clean style
    plt.style.use("seaborn-v0_8-notebook") 
    fig, ax = plt.subplots(figsize=(12, 6))

    # ---- 1️⃣ Prepare data ----
    df['date'] = pd.to_datetime(df['date']) 
    df = df.sort_values("date")
    df["rolling_avg"] = df["mood_score"].rolling(rolling_window, min_periods=1).mean()

    # Create a base plot of the daily mood score line (without markers initially)
    ax.plot(df["date"], df["mood_score"], color="#005a9c",
            label="Daily Mood Score (1=Low → 5=High)", lw=2.5, zorder=5)
    
    # Plot the rolling average line
    ax.plot(df["date"], df["rolling_avg"], linestyle="-", color="#ff8c00",
            label=f"{rolling_window}-Day Rolling Avg", lw=2, alpha=0.8, zorder=4)

    # ---- 2️⃣ Mood zones ----
    high_mood_color = "#e5f5e5"
    moderate_mood_color = "#fff7bc" 
    low_mood_color = "#fbe7e8"
    
    ax.axhspan(4, 5.5, facecolor=high_mood_color, alpha=1.0, label="High Mood (4–5)", zorder=1)
    ax.axhspan(3, 4, facecolor=moderate_mood_color, alpha=1.0, label="Moderate Mood (3–4)", zorder=1)
    ax.axhspan(0.5, 3, facecolor=low_mood_color, alpha=1.0, label="Low Mood (1–3)", zorder=1)
    
    ax.axhline(4, color='gray', linestyle=':', linewidth=0.5, zorder=2)
    ax.axhline(3, color='gray', linestyle=':', linewidth=0.5, zorder=2)

    # ---- 3️⃣ Labels & style (omitted for brevity) ----
    ax.set_title("Mood Trend Over Time", fontsize=18, weight="bold", pad=20)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Mood Score", fontsize=12)
    
    ax.set_xticks(df["date"])
    date_labels = [d.strftime('%m-%d') for d in df["date"]] 
    ax.set_xticklabels(date_labels, rotation=35, ha="right", fontsize=10)
    
    ax.set_yticks(np.arange(1, 6))
    plt.ylim(0.5, 5.5)
    
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = {}
    for h, l in zip(handles, labels):
        unique_labels[l] = h
        
    ax.legend(unique_labels.values(), unique_labels.keys(), 
              loc="upper center", bbox_to_anchor=(0.5, -0.25), 
              ncol=5, fontsize=10, frameon=True, fancybox=True, shadow=True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.grid(axis='x', visible=False)

    # ---- 4️⃣ Smart annotation and cluster differentiation logic ----
    texts = []
    
    if annotate_patterns:
        # Create a dictionary to hold annotation data for each date
        annotation_data = {}
        
        # 1. Collect all annotation data from patterns
        for p in annotate_patterns:
            for evidence_entry in p.get("evidence", []):
                
                evidence_date_entry = evidence_entry.get("date")
                mood_word = evidence_entry.get("mood", "N/A") 
                cluster_id = evidence_entry.get("cluster", -1) 

                if evidence_date_entry:
                    if isinstance(evidence_date_entry, pd.Timestamp):
                        date_str = evidence_date_entry.strftime('%Y-%m-%d')
                    else:
                        date_str = str(evidence_date_entry).split('T')[0]
                    
                    if date_str not in annotation_data:
                        d = df.loc[df['date'].dt.strftime('%Y-%m-%d') == date_str, 'date'].iloc[0] if not df.loc[df['date'].dt.strftime('%Y-%m-%d') == date_str, 'date'].empty else None
                        score = df.loc[df['date'].dt.strftime('%Y-%m-%d') == date_str, 'mood_score'].iloc[0] if not df.loc[df['date'].dt.strftime('%Y-%m-%d') == date_str, 'mood_score'].empty else None
                        
                        if d is not None and score is not None:
                            # Use the highest cluster ID if multiple patterns reference the same point
                            annotation_data[date_str] = {
                                'date': d, 
                                'score': score, 
                                'mood': mood_word, 
                                'cluster_id': cluster_id
                            }
                        
        # 2. Iterate through collected data to plot points and add text
        for date_str, data in annotation_data.items():
            d = data['date']
            score = data['score']
            desc = data['mood'].capitalize()
            cluster_id = data['cluster_id']

            # Determine point styling
            if cluster_id != -1:
                point_color = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]
                markersize = 9 # Larger size for clustered points
            else:
                point_color = '#005a9c' # Default color for base line points (temporal patterns)
                markersize = 6
            
            # Plot the differentiated point (overlaying the original line markers)
            ax.plot(d, score, 
                    marker="o", 
                    color=point_color, 
                    markersize=markersize, 
                    zorder=7, # Higher zorder to ensure it's on top
                    linestyle='') # No line, just the marker
            
            # Create text annotation
            txt = ax.text(
                d,
                score,
                desc,
                fontsize=9,
                ha="center", 
                va="bottom",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#005a9c", lw=0.7, alpha=0.9, color="#005a9c")
            )
            texts.append(txt)

        # 3. Apply adjustment to annotations
        adjust_text(
            texts,
            ax=ax,
            expand_text=(1.1, 1.3), 
            expand_points=(1.1, 1.3),
            arrowprops=dict(arrowstyle="->", color="#333333", lw=0.7),
            only_move={'points':'y', 'texts':'xy'}, 
            force_points=0.6, 
            force_text=0.7,   
            lim=1500 
        )

    plt.tight_layout(rect=[0, 0.15, 1, 1])
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    return output_path