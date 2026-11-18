# COBRA: Financial Transaction Anomaly & Coordinated Behavior Analytics

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/ML-Isolation%20Forest-orange)
![Time Series](https://img.shields.io/badge/Time--Series-ARIMA%20(Z--Score)-teal)
![Graph Analytics](https://img.shields.io/badge/Graph-NetworkX%20%7C%20Louvain-blueviolet)
![Explainable AI](https://img.shields.io/badge/XAI-SHAP%20TreeExplainer-green)
![Visualization](https://img.shields.io/badge/Dashboards-Plotly%20Interactive-red)

## Executive Summary
Traditional financial fraud monitoring relies heavily on single-account rule-based thresholds. However, modern financial crime rings systematically bypass these controls through **smurfing** and synchronized multi-account mule networks, where individual nodes exhibit entirely normal transactional behaviors in isolation. 

This repository houses the core **Data Engineering, Graph Analytics, Unsupervised Anomaly Detection, Explainable AI (XAI), and Interactive Forensic Visualization** pipeline for **COBRA (Coordinated Behavior Analysis and Detection System)**. Benchmarked on the **6.3M-row PaySim Synthetic Financial Dataset**, the engine structures transaction logs into relational networks, surfaces temporal volume anomalies, computes a normalized **0–100 Coordination Score**, and generates local SHAP explanations alongside standalone interactive Plotly forensic dashboards.

📄 **[Read the Full Technical Report](COBRA_Technical_Report.pdf)**

---

## Analytical Workflow & Fraud Pattern Diagrams

### 1. End-to-End Data Science & XAI Pipeline
```text
[Raw PaySim Log: 6.3M Rows]
           │
           ▼  (data_exploration.py & feature_engineering.py)
┌──────────────────────────────────────────────────────────┐
│ 1. Domain Filtering & Edge Aggregation                   │
│    • Filter: TRANSFER & CASH_OUT vectors only            │
│    • Engineer: hour_of_day, day, balance_drained         │
│    • GroupBy (nameOrig, nameDest) -> Edge Metrics        │
└──────────┬───────────────────────────────────┬───────────┘
           │                                   │
           ▼  (graph_analytics.py)             ▼  (main.py - ARIMA)
┌──────────────────────────────┐    ┌──────────────────────────────────────┐
│ 2A. Graph & Community Engine │    │ 2B. Temporal Burst Forecaster        │
│ • Directed Graph (NetworkX)  │    │ • Hourly Volume Aggregation          │
│ • PageRank, In/Out Degree    │    │ • ARIMA Baseline Expectation         │
│ • Louvain Community Detection│    │ • Residual Z-Score > 3 Burst Flag    │
└──────────┬───────────────────┘    └──────────────────┬───────────────────┘
           │                                           │
           └─────────────────────┬─────────────────────┘
                                 ▼  (anomaly_detection.py)
┌──────────────────────────────────────────────────────────────────────────┐
│ 3. Unsupervised Scoring & Explainable AI (XAI)                           │
│    • Isolation Forest trained on structural + behavioral features        │
│    • Normalized 0–100 Coordination Score (Alert Threshold > 80)          │
│    • SHAP TreeExplainer Waterfall Plot for top-flagged mule actors       │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
                                 ▼  (dashboard_cycles.py & dashboard_visuals.py)
┌──────────────────────────────────────────────────────────────────────────┐
│ 4. Interactive Forensic Dashboards (HTML)                                │
│    • dashboard_anomalies.html       (Top 50 Suspect Cluster Network)     │
│    • dashboard_chart_temporal.html  (ARIMA vs. Actual Volume Spikes)     │
│    • dashboard_chart_scores.html    (In-Degree vs. Out-Degree Scatter)   │
└──────────────────────────────────────────────────────────────────────────┘
```

* **Diagram Explanation:** The architecture transforms raw payment logs into structured graph topologies and time-series models. Structural node attributes (`in_degree`, `out_degree`, `PageRank`) and behavioral aggregates (`total_sent`, `time_span`, `balance_drained`) are processed via an unsupervised **Isolation Forest**. Concurrently, an **ARIMA** time-series model establishes baseline transaction throughput to isolate abnormal volume spikes ($Z > 3$). Finally, **SHAP (`TreeExplainer`)** breaks down individual risk predictions into human-auditable feature contributions, while **Plotly** exports standalone interactive HTML workspaces.

---

### 2. Graph Topology & Fraud Pattern Detection Logic
```text
   [Fan-In Collection Hub]               [Pass-Through Mule Chain]
    Acc_A ──┐                            Acc_1 ──► Acc_2 ──► Acc_3
    Acc_B ──┼──► [Mule Sink]               (Rapid liquidity layering
    Acc_C ──┘   (High In-Degree,            with zero-balance drain)
                 Low Out-Degree)
```

* **Diagram Explanation:** By mapping origin-destination payment flows (`nameOrig` $\rightarrow$ `nameDest`) into a directed graph (`nx.DiGraph`), the model differentiates legitimate high-frequency accounts from structural fraud signatures—such as fan-in collection sinks (where numerous smurfed accounts funnel funds into a single entity) and rapid pass-through layering chains.

---

## Visual Outputs & Forensic Dashboard Breakdown

Each visual artifact generated by the pipeline supports granular compliance and investigator triage:

1. **High-Risk Cluster Topology (`dashboard_anomalies.html` — via `dashboard_cycles.py`)**
   * **What it shows:** An interactive directed network visualization mapping the top 50 highest-risk accounts (`coordination_score`) and their immediate transactional counterparties. Nodes are shaded on a continuous red severity gradient.
   * **Investigative Insight:** Instantly reveals hidden sub-communities, star-shaped distribution hubs, and cyclical laundering loops that tabular reports obscure.

2. **Temporal Volume Burst Monitor (`dashboard_chart_temporal.html` — via `dashboard_visuals.py`)**
   * **What it shows:** A dual-series time-series graph contrasting actual hourly transaction volume against ARIMA baseline predictions across simulation hours (`step`), highlighting statistical anomalies where residual bounds cross $Z > 3$.
   * **Investigative Insight:** Differentiates natural diurnal business peaks from coordinated, malicious liquidity drains.

3. **Coordination Score & Degree Scatter (`dashboard_chart_scores.html` — via `dashboard_visuals.py`)**
   * **What it shows:** A multi-dimensional bubble scatter plot mapping incoming transaction volume (`in_degree`) against outgoing transactions (`out_degree`) for flagged accounts (`coordination_score > 80`), sized by risk magnitude.
   * **Investigative Insight:** Classifies suspicious entities into distinct behavioral archetypes—separating collection sinks from smurf distributors and pass-through nodes.

4. **SHAP Waterfall Evidence Plot (`evidence_<account_id>.png` — via `anomaly_detection.py`)**
   * **What it shows:** A local SHAP waterfall decomposition for the highest-scoring anomaly actor, tracking how each engineered feature pushes the model from expected baseline risk to an extreme anomaly score.
   * **Investigative Insight:** Eliminates "black-box" model hesitancy by delivering clear, mathematical proof for why an alert was generated.

---

## Tools, Technologies & Methodologies

| Analytic Stage | Technologies & Libraries | Methodological Role |
| :--- | :--- | :--- |
| **Data Engineering** | `Python`, `Pandas`, `NumPy` | Ingestion, memory profiling, and high-risk filtering of 6.3M records (`TRANSFER`, `CASH_OUT`), followed by origin-destination edge reduction. |
| **Graph Analytics** | `NetworkX`, `python-louvain` | Directed multigraph modeling (`DiGraph`), centrality calculations, and modularity-optimized community discovery. |
| **Anomaly & Time-Series** | `Scikit-Learn`, `Statsmodels` | Unsupervised **Isolation Forest** modeling (`contamination=0.02`) and **ARIMA** time-series forecasting with residual $Z$-score filtering. |
| **Explainable AI (XAI)** | `SHAP`, `Matplotlib` | Tree-based model explainer generating precise local feature attribution charts for top threats. |
| **Interactive Visuals** | `Plotly Express`, `Plotly Graph Objects` | Generation of responsive, zero-dependency HTML diagnostic dashboards with custom hover tooltips. |

---

## Study Outcomes & Key Findings

* **Class Imbalance Realities:** Exploratory analysis verified extreme class imbalance within the 6.3M records, isolating **8,213 verified fraud cases (~0.13%)** exclusively contained within `TRANSFER` and `CASH_OUT` vectors.
* **Zero-Day Pattern Recognition:** Leveraging structural graph metrics (`in_degree`, `out_degree`, `time_span`) alongside isolation forests successfully captured sophisticated mule behavior without depending on historical fraud labels.
* **Actionable Alert Prioritization:** Consolidating multi-variable network and temporal deviations into a unified **0–100 Coordination Score** (with high-risk filters set at $>80$) paired with automated SHAP visual evidence drastically minimizes investigator alert fatigue and review cycles.

---

## Repository File Guide & Local Quickstart

### Directory Structure
```text
├── main.py                          # End-to-end analytical pipeline orchestrator
├── data_exploration.py              # Dataset schema validation, missing values & EDA checks
├── feature_engineering.py           # Liquidity vector filtering & origin-destination aggregation
├── graph_analytics.py               # NetworkX graph creation, centrality & community mapping
├── anomaly_detection.py             # Isolation Forest training & SHAP waterfall chart export
├── dashboard_cycles.py              # Interactive Plotly network layout for top 50 suspects
├── dashboard_visuals.py             # Interactive Plotly ARIMA time-series & scatter dashboards
├── processed_transaction_edges.csv  # Aggregated origin-destination network edge parameters
├── node_features.csv                # Computed graph centrality & behavioral node attributes
├── arima_temporal_anomalies.csv     # Hourly transaction aggregates, ARIMA fits & Z > 3 flags
├── final_coordination_scores.csv    # Final 0-100 Coordination Scores & anomaly classifications
├── dashboard_anomalies.html         # Interactive Network Cluster Dashboard
├── dashboard_chart_temporal.html    # Interactive Temporal Burst Chart
├── dashboard_chart_scores.html      # Interactive Coordination Score Scatter Plot
├── requirements.txt                 # Project python dependencies
└── .gitignore                       # Excludes raw PaySim CSV and local IDE cache
```

### Local Setup & Quickstart

1. **Clone the Repository & Set Up Environment**
   ```bash
   git clone https://github.com/<your-username>/cobra-fraud-analytics.git
   cd cobra-fraud-analytics
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Re-running Upstream Extraction**
   * Download the original **PaySim Financial Dataset** (`PS_20174392719_1491204439457_log.csv`) and place it in the root directory.
   * *Note: Because the raw dataset (~482 MB) exceeds GitHub's file storage limits, it is omitted via `.gitignore`. Pre-computed intermediate CSVs are included so all evaluation, modeling, and visualization scripts execute immediately out of the box.*

4. **Execute the Pipeline**
   ```bash
   python main.py
   ```