# 🧠 Zumlo — Mood Pattern Analyzer + Micro-Action Recommender

### A part of **Zumlo — The Mental Health Ecosystem**

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <repository_url>
cd mood_pattern_project
2️⃣ Create and Activate a Virtual Environment
bash
Copy code
python -m venv .venv
source .venv/bin/activate       # (Windows: .venv\Scripts\activate)
4️⃣ Prepare Input Data
Place your mood logs file (e.g., sample_mood_logs.json) in the data/ folder.
Each entry must include:

### 4️⃣ Prepare Input Data
Place your mood logs file (e.g., sample_mood_logs.json) in the data/ folder.
Each entry must include:
Detected Patterns JSON: outputs/detected_patterns.json

Mood Trend Plot: outputs/mood_trend.png

🧠 Design Decisions
Copy code
src/
├── data_loader.py           # Load and preprocess mood logs
├── mood_mapper.py           # Map moods to numeric scores
├── pattern_detector.py      # Detect temporal and contextual mood patterns
├── micro_action_generator.py# Generate empathetic, safe micro-actions
├── visualizer.py            # Generate mood trend chart
├── utils.py                 # Helper functions for saving results
└── main.py                  # Orchestrator script
2. Pattern Detection
Combines rule-based methods (e.g., day-of-week mood dips) with lightweight ML (clustering via embeddings).


3. Micro-Action Generation
Generates 3 short, safe, and non-clinical actions per detected pattern.

Designed to encourage daily mindfulness and positive reinforcement.

Randomized selection ensures variety while maintaining relevance to mood type.

4. Visualization
Uses matplotlib to create a time-series plot of mood scores.

The plot helps users visually track mood trends across days.

5. Privacy & Safety
No personal or sensitive data is stored.

All outputs are non-medical, empathetic, and judgment-free.

Optionally, the system can flag patterns indicating distress with a prompt to seek professional help.

6. Reproducibility
Deterministic results for the same dataset.

Clear separation of data, logic, and visualization.

Output files and charts are automatically generated in the outputs/ directory.

7. Extensibility
Can easily integrate additional mood attributes or environmental factors (time, activity).

Open for connecting with APIs or UI dashboards for real-time visualization.

✅ Summary
This project provides a fully functional pipeline to:

Ingest daily mood logs

Detect emotional patterns

Recommend micro-actions

Visualize mood trends

It is built to be lightweight, explainable, and privacy-friendly — suitable for extending into a larger Mental Health Ecosystem such as Zumlo.