import matplotlib.pyplot as plt
import numpy as np

# ---- CONFIG ----
labels = ["Commits", "Code Review", "Pull Requests", "Issues"]
values = [45, 35, 18, 2]  # adjust or automate later
bg_color = "#0d1117"
grid_color = "#30363d"
text_color = "#c9d1d9"
accent = "#2ea043"

# ---- RADAR SETUP ----
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
values += values[:1]
angles = np.concatenate([angles, angles[:1]])

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.plot(angles, values, color=accent, linewidth=2)
ax.fill(angles, values, color=accent, alpha=0.4)

ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels, color=text_color, fontsize=11)
ax.set_yticklabels([])
ax.spines["polar"].set_color(grid_color)

plt.savefig("activity-radar.svg", format="svg", facecolor=bg_color)
plt.close()
