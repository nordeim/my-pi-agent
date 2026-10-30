#!/usr/bin/env python3
"""Rubric scorecard heatmap for the skills audit report (IG-1 Ink Gold palette)."""
import os
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["axes.unicode_minus"] = False

DIMENSIONS = [
    "Sourcing & verification",
    "Fact / judgment separation",
    "GAAP vs non-GAAP bridge",
    "Reference-data accuracy",
    "Attribution methodology",
    "Model governance (SR 11-7)",
    "Audit gates & QA automation",
    "Compliance posture",
    "Reproducibility & hygiene",
    "Deliverable craftsmanship",
]
SKILLS = ["Skill 1\nRCA deck", "Skill 2\nPost-mortem", "Skill 3\nResearch note"]
# Auditor assessment (Reasoned), 0-5 anchors defined in the report body.
SCORES = np.array([
    [5.0, 3.5, 3.5],   # Sourcing & verification
    [4.0, 4.0, 4.0],   # Fact/judgment separation
    [5.0, 5.0, 2.5],   # GAAP vs non-GAAP bridge
    [4.0, 3.0, 2.0],   # Reference-data accuracy
    [5.0, 4.0, 3.5],   # Attribution methodology
    [4.0, 1.0, 2.5],   # Model governance
    [4.0, 1.0, 1.5],   # Audit gates & QA
    [4.5, 1.5, 4.0],   # Compliance posture
    [4.0, 2.0, 3.0],   # Reproducibility & hygiene
    [5.0, 3.5, 3.5],   # Deliverable craftsmanship
])

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "assets" / "rubric_heatmap.png"
os.makedirs(OUT.parent, exist_ok=True)

fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(SCORES, cmap="YlOrBr", aspect="auto", vmin=0, vmax=5)

ax.set_xticks(range(len(SKILLS)))
ax.set_yticks(range(len(DIMENSIONS)))
ax.set_xticklabels(SKILLS, fontsize=11)
ax.set_yticklabels(DIMENSIONS, fontsize=10)

for i in range(len(DIMENSIONS)):
    for j in range(len(SKILLS)):
        val = SCORES[i, j]
        color = "white" if val > SCORES.max() * 0.72 else "black"
        ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                fontsize=10, color=color)

fig.colorbar(im, ax=ax, shrink=0.8, label="Score (0 = absent, 5 = institutional grade)")
ax.set_title("Institutional-readiness scorecard (auditor assessment)",
             fontsize=13, pad=15)

fig.savefig(OUT, dpi=200, bbox_inches="tight", pad_inches=0.3,
            facecolor="white", edgecolor="none")
plt.close(fig)
print("saved", OUT)
print("averages:", [round(SCORES[:, j].mean(), 2) for j in range(3)])
