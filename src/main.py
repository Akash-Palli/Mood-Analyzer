from data_loader import load_mood_data
from mood_mapper import map_mood_to_score
from pattern_detector import detect_temporal_patterns, cluster_note_patterns
from micro_action_generator import generate_micro_actions
from visualizer import plot_mood_trend
from utils import save_json

def main():
    df = load_mood_data("data/sample_mood_logs.json")
    df["mood_score"] = df["mood"].apply(map_mood_to_score)

    temporal_patterns = detect_temporal_patterns(df)
    note_patterns = cluster_note_patterns(df)
    all_patterns = temporal_patterns + note_patterns

    final_output = {"patterns": []}
    for pattern in all_patterns:
        pattern["micro_actions"] = generate_micro_actions(pattern["description"])
        final_output["patterns"].append(pattern)

    # ✅ Enhanced Visualization Call (with pattern annotations)
    plot_path = plot_mood_trend(
        df,
        output_path="outputs/mood_trend.png",
        rolling_window=3,
        annotate_patterns=final_output.get("patterns", [])
    )
    final_output["plot"] = plot_path
    save_json(final_output, "outputs/detected_patterns.json")

    print("✅ Analysis complete! Results saved in outputs/")

if __name__ == "__main__":
    main()
