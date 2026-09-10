KneeWS — FYP proposal defence pack
Noise-Aware Weak Supervision from Multilingual Radiology Reports
for Multi-Label Knee MRI Analysis
==================================================================

Everything here comes in two versions:

  PRIMARY   — the registered idea. Report reliability is measured
              against the 58 expert-labelled studies.

  OPTION B  — the secondary method held in reserve. The same
              reliability is estimated from the model's own confident
              disagreements, so all 58 expert studies stay sealed and
              can act as an independent referee.

The registered title, scope, ten features and CCP mapping are
identical under both. Only the estimator inside Feature 5 differs.


01_Decks
--------
KneeWS_Proposal_Defence_PRIMARY.pptx
KneeWS_Proposal_Defence_OPTION_B.pptx

Exactly ten slides each, matching the FYP Committee's prescribed
structure, with a numbered badge on every slide so the panel can tick
against it. Speaker notes are written on each slide.

Before the defence: fill in the member names and supervisor on
slide 1 of both decks. They are currently placeholders.


02_Prototypes
-------------
Walkthrough/  <- PRESENT THESE
  kneews_walkthrough.html
  kneews_walkthrough_optionb.html

  Six steps, one idea each. Arrow keys or the Back / Next buttons move
  between them. Every step ends in a coloured band carrying the line to
  say out loud.

  Suggested route, about 90 seconds:
    Step 1 — press "Read the report", land on 4 named / 8 never mentioned
    Step 2 — toggle Standard practice against KneeWS
    Step 3 — the four rules (in Option B, press "Reveal the 58")
    Step 5 — toggle the two models; the striped bar is an abstention

Dashboard/    <- keep open in a second tab for questions
  kneews_primary.html
  kneews_optionb.html

  Eleven screens mapped one-to-one onto the ten registered features.
  Use if the panel asks to see disagreement cases, the labelling
  workbench, or institution onboarding.

All four files open in any browser by double-clicking. No internet
connection, no install, no server required.


03_Document
-----------
KneeWS_Project_Record.docx

25 pages: the registered project, the system architecture with seven
diagrams, what the research established, Option B in full with its
mathematics and a thirteen-step build order, the work plan and risks.


04_Diagrams
-----------
The seven architecture figures as PNGs, in case you need them for the
report, the poster, or a slide of your own.


A NOTE TO SAY OUT LOUD DURING THE DEMO
--------------------------------------
Every number, scan, patient and name in the prototypes is synthetic.
No image model has been trained yet. What the proof of concept
establishes is feasibility and two design decisions — partial pooling
instead of per-finding estimation, and open-weight in-notebook
labelling — not results.

The dataset figures quoted throughout (4,407 studies, 58 with expert
labels, 82.5% report-versus-expert agreement) are transcribed from
participant repositories and host posts. Verify them first-hand on the
Kaggle data tab in week one, before anything is built on them.
