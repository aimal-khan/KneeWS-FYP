# KneeWS — Noise-Aware Weak Supervision from Multilingual Radiology Reports for Multi-Label Knee MRI Analysis

> **Final Year Project (FYP) Proposal Defence Pack & Repository**  
> Noise-Aware Weak Supervision for Knee MRI Multi-Label Diagnostic Analysis

---

## 📌 Overview

**KneeWS** explores noise-aware weak supervision using multilingual radiology reports for multi-label knee MRI interpretation. The materials and architectures in this repository are structured around two distinct operational designs:

1. **PRIMARY (Registered Method)**: Report reliability is measured against 58 expert-labelled studies.
2. **OPTION B (Secondary / Reserve Method)**: Report reliability is estimated internally from the model's own confident disagreements, keeping all 58 expert-labelled studies sealed for an independent evaluation/referee role.

> *Note:* The registered title, project scope, 10 key features, and CCP mapping are identical under both options. Only the reliability estimator inside Feature 5 differs.

---

## 📂 Repository Structure

```text
├── 01_Decks/              # Presentation slides for proposal defence
│   ├── KneeWS_Proposal_Defence_PRIMARY.pptx
│   └── KneeWS_Proposal_Defence_OPTION_B.pptx
├── 02_Prototypes/         # Zero-dependency interactive web prototypes
│   ├── Walkthrough/       # Guided 6-step demo for live presentation
│   │   ├── kneews_walkthrough.html
│   │   └── kneews_walkthrough_optionb.html
│   └── Dashboard/         # 11-screen feature explorer for Q&A
│       ├── kneews_primary.html
│       └── kneews_optionb.html
├── 03_Document/           # Comprehensive 25-page project record
│   └── KneeWS_Project_Record.docx
├── 04_Diagrams/           # High-resolution architectural figures (PNG)
│   ├── fig1_product_flow.png
│   ├── fig2_training_pipeline.png
│   ├── fig3_four_states.png
│   ├── fig4_system_layers.png
│   ├── fig5_experiment.png
│   ├── fig6_option_b.png
│   └── fig7_fallback.png
└── _archive/              # Archived exploratory scraping scripts & legacy chats
    └── legacy_research/
```

---

## 🚀 Presentation & Defence Guide

### 1. Presentation Slides (`01_Decks/`)
- Exactly 10 slides each, adhering strictly to the FYP Committee's prescribed structure.
- Numbered badge on every slide for easy scoring by the defence panel.
- Speaker notes included on every slide.
- **Action Item:** Fill in group member names and supervisor name on Slide 1 of both decks prior to presentation.

### 2. Interactive Prototypes (`02_Prototypes/`)
All prototypes are self-contained HTML/JS applications. Double-click to open in any web browser without needing a web server or internet connection.

* **Walkthrough (`02_Prototypes/Walkthrough/`)** *(Recommended for initial ~90s pitch)*
  - Step 1: Press *"Read the report"* (identifies 4 named vs 8 unmentioned findings).
  - Step 2: Toggle standard practice vs KneeWS.
  - Step 3: Four supervision rules (or *"Reveal the 58"* in Option B).
  - Step 5: Toggle between models (striped bar indicates model abstention).
* **Dashboard (`02_Prototypes/Dashboard/`)** *(Keep ready in a background browser tab)*
  - Features 11 screens mapped 1:1 against the 10 registered features.
  - Useful if the panel asks for specific details on disagreement cases, the labelling workbench, or multi-institution onboarding.

### 3. Architecture Diagrams (`04_Diagrams/`)
- `fig1_product_flow.png`: High-level clinical and technical pipeline flow.
- `fig2_training_pipeline.png`: Weakly-supervised model training stage.
- `fig3_four_states.png`: Label state space and supervision taxonomy.
- `fig4_system_layers.png`: System architecture and component layering.
- `fig5_experiment.png`: Experimental setup and evaluation benchmarks.
- `fig6_option_b.png`: Option B agreement/disagreement estimator architecture.
- `fig7_fallback.png`: Fallback handling and failover decision path.

---

## ⚠️ Important Presentation Notes

> "Every number, scan, patient and name in the prototypes is synthetic. No image model has been trained yet. What the proof of concept establishes is feasibility and two design decisions — partial pooling instead of per-finding estimation, and open-weight in-notebook labelling — not results.
> 
> The dataset figures quoted throughout (4,407 studies, 58 with expert labels, 82.5% report-versus-expert agreement) are transcribed from participant repositories and host posts. Verify them first-hand on the Kaggle data tab in week one, before anything is built on them."
