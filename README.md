# 🌤️ Mood Analyzer  
A simple, explainable, and safe mood-pattern analysis system

**Mood Analyzer** is a lightweight Python-based system that processes daily mood logs, detects emotional patterns, identifies mood trends, clusters similar notes using sentence embeddings, and generates empathetic micro-actions.  
The project is fully modular, easy to extend, and aligned with all constraints outlined in the assignment.

---

## 📌 Key Features

### 1. Daily Mood Log Processing
- Reads daily mood logs from a JSON file  
- Extracts **date**, **mood**, and optional **notes**  
- Converts moods into normalized numeric scores  

---

### 2. Temporal Pattern Detection
- Identifies **weekday-based** mood dips and peaks  
- Automatically extracts supporting evidence  
- Generates **safe, empathetic micro-actions** for each pattern  

---

### 3. Embedding-Based Note Clustering
- Uses **SentenceTransformer (all-MiniLM-L6-v2)**  
- Clusters notes into similar emotional groups  
- Computes a **confidence score** per cluster  
- Summarizes common mood trends within each group  

---

### 4. Visual Mood Trend Plot
- Clean, readable **Matplotlib** line graph  
- Automatically adjusts legend placement  
- Displays mood scores (**1–5**) clearly  
- Saves output to:  outputs/mood_trend.png

---

### 5. Safe, Empathetic Micro-Actions
- Avoids medical or clinical suggestions  
- Uses supportive, non-judgmental language  
- Optional fallback micro-action:
- Reach out to a trusted person or mental health professional when patterns show persistent distress  

---

### 6. Jupyter Notebook Interactive Demo
Available at:  notebooks/mood_analysis_demo.ipynb

---

### 7. Unit Tests
- Includes basic unit tests for core pattern detection  
- Ensures reproducibility and correctness  

---

# 🚀 How to Run the Project

## 1. Clone the Repository
```bash
git clone https://github.com/Akash-Palli/Mood-Analyzer.git
cd Mood-Analyzer
```
## 2. Create and Activate a Virtual Environment
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
## 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Run the Analyzer
```bash
python src/main.py
```

## 📤 Output Files Generated

| Output File | Description |
|------------|-------------|
| `outputs/analysis.json` | All detected patterns, clusters, and generated micro-actions |
| `outputs/mood_trend.png` | Saved mood visualization plot |


## 📝 (Optional) Launch Jupyter Notebook
```bash
jupyter notebook notebooks/mood_analysis_demo.ipynb
```

---
## 🧪 Run Unit Tests
```bash
pytest -v
```

## 📂 Project Structure
```text
Mood-Analyzer/
│── data/
│   └── sample_mood_logs.json
│
│── notebooks/
│   └── mood_analysis_demo.ipynb
│
│── outputs/
│   ├── analysis.json
│   └── mood_trend.png
│
│── src/
│   ├── data_loader.py
│   ├── mood_mapper.py
│   ├── pattern_detector.py
│   ├── micro_action_generator.py
│   ├── visualizer.py
│   ├── utils.py
│   └── main.py
│
│── tests/
│   └── test_pattern_detector.py
│
│── requirements.txt
│── README.md
│── .gitignore
```
## 🧠 System Workflow (End-to-End)

### 1. Load Data
- JSON logs are parsed using `data_loader.py`

### 2. Map Mood → Score
- `mood_mapper.py` converts moods to normalized numeric scores (1–5)

### 3. Detect Temporal Patterns
- `pattern_detector.detect_temporal_patterns`
- Identifies weekday highs/lows and recurring mood cycles

### 4. Cluster Notes (Bonus Feature)
- Uses sentence embeddings  
- Applies K-Means clustering  
- Generates a confidence score per cluster  

### 5. Generate Micro-Actions
- Handled by `micro_action_generator.py`  
- Produces short, empathetic, non-medical suggestions  

### 6. Visualize Mood Trend
- `visualizer.py` creates a clean Matplotlib line graph  

### 7. Save Results
All outputs are saved to:  
- `outputs/analysis.json`  
- `outputs/mood_trend.png`

## 🧩 Design Decisions

This project follows a clarity-first, safety-first, and explainability-driven design philosophy. Every component was intentionally chosen to balance simplicity, interpretability, and functional effectiveness.

---

### 1. Simple, Explainable Mood Scoring Instead of ML Models  
**Decision:**  
Use a fixed mapping from mood labels → numeric mood scores (`mood_mapper.py`).

**Reason:**  
- Keeps the system interpretable  
- No need for mood-classification ML models  
- Ensures deterministic, reproducible scoring  
- Aligns with requirement: *“simple, explainable methods for pattern detection”*

---

### 2. Rule-Based Temporal Pattern Detection  
**Decision:**  
Use weekday-level aggregation to detect mood dips/peaks (`detect_temporal_patterns()`).

**Reason:**  
- Avoids black-box ML  
- Easy to justify: “Wednesdays have lowest average mood”  
- Captures meaningful behavior patterns without overfitting  
- Matches requirement: lightweight, explainable pattern extraction  

---

### 3. Optional ML Only for Notes Clustering  
**Decision:**  
Use SentenceTransformer (`all-MiniLM-L6-v2`) + KMeans for clustering notes (`cluster_note_patterns()`).

**Reason:**  
- Free-text notes require semantic understanding  
- KMeans offers transparent, interpretable grouping  
- Feature remains optional (bonus task)  
- Confidence scores improve transparency of cluster quality  

---

### 4. Confidence Scores for Transparency  
**Decision:**  
Confidence score = weighted combination of:  
- cluster cohesion (average embedding distance)  
- number of evidence points  

**Reason:**  
- Makes ML-derived insights explainable  
- Helps users understand pattern strength  
- Avoids overstating weak clusters  

---

### 5. Safe, Non-Clinical Micro-Actions  
**Decision:**  
Generate empathetic, simple, non-medical micro-actions (`micro_action_generator.py`).

**Reason:**  
- Meets required safety constraints  
- Avoids mental-health risk  
- Provides gentle, supportive nudges  
- Includes fallback suggestion when persistent distress is observed  

---

### 6. Minimal Dependencies, Fully Offline Capable  
**Decision:**  
Use lightweight libraries only:  
- pandas  
- matplotlib  
- scikit-learn  
- sentence-transformers  

**Reason:**  
- Avoids heavy LLM/API dependencies  
- Fully offline execution  
- Easy installation and cross-platform reproducibility  

---

### 7. Clean, User-Friendly Mood Visualization  
**Decision:**  
Plot only:  
- mood score trend  
- optional rolling mean  
- mood markers (without cluttered annotations)

**Reason:**  
- Enhances readability  
- Avoids annotation overlaps  
- Keeps the user's focus on mood changes  

---

### 8. Modular Architecture  
**Decision:**  
Split logic into small, purpose-driven modules:

| Module | Purpose |
|--------|---------|
| `data_loader.py` | Handles input loading and date parsing |
| `mood_mapper.py` | Normalizes mood labels into numeric scores |
| `pattern_detector.py` | Detects weekday patterns and clusters notes |
| `micro_action_generator.py` | Generates safe, supportive micro-actions |
| `visualizer.py` | Produces clean Matplotlib plots |
| `main.py` | Orchestrates the full workflow |

**Reason:**  
- Improves testability  
- Enhances maintainability and extendibility  
- Ensures clean abstraction boundaries  

---

### 9. Jupyter Notebook Demo for Interpretability  
**Decision:**  
Include an interactive notebook (`notebooks/mood_analysis_demo.ipynb`).

**Reason:**  
- Supports debugging and exploration  
- Helps visually inspect clusters and patterns  
- Improves assignment presentation and usability  

---

### 10. Basic Unit Tests for Core Logic  
**Decision:**  
Unit tests target only deterministic logic (`tests/test_pattern_detector.py`).

**Reason:**  
- ML clusters are non-deterministic → not suitable for strict testing  
- Ensures rule-based logic (weekday pattern detection) remains reliable  

---

## ✔ Summary of Design Principles

| Principle | How It Was Achieved |
|----------|----------------------|
| **Explainability** | Rule-based scoring, weekday analysis, transparent clustering |
| **Safety** | Empathetic micro-actions, no clinical content |
| **Simplicity** | Minimal dependencies, modular code, simple scoring |
| **Reproducibility** | Deterministic logic, fixed mappings, no API calls |
| **Usability** | Clean visualization, notebook demo, structured outputs |


