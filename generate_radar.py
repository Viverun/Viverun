from github import Github
import matplotlib.pyplot as plt
import numpy as np
import os

# ===== CONFIG =====
USERNAME = "Viverun"  # <-- MUST be your GitHub username
BG = "#0d1117"
GRID = "#30363d"
TEXT = "#c9d1d9"
ACCENT = "#2ea043"

# ===== AUTH =====
token = os.getenv("GH_TOKEN")
g = Github(token)
user = g.get_user(USERNAME)

# ===== FETCH RECENT ACTIVITY (GitHub API LIMIT SAFE) =====
commits = prs = issues = reviews = 0

for event in user.get_events():
    if event.type == "PushEvent":
        commits += len(event.payload.get("commits", []))
    elif event.type == "PullRequestEvent" and event.payload["action"] == "opened":
        prs += 1
    elif event.type == "IssuesEvent" and event.payload["action"] == "opened":
        issues += 1
    elif event.type == "PullRequestReviewEvent":
        reviews += 1

raw = {
    "Commits": commits,
    "Code Review": reviews,
    "Pull Requests": prs,
    "Issues": issues,
}

total = sum(raw.values()) or 1
labels = list(raw.keys())
values = [round(v / total * 100, 1) for v in raw.values()]

# ===== RADAR CHART =====
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
angles = np.concatenate([angles, angles[:1]])
values = values + values[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.plot(angles, values, color=ACCENT, linewidth=2)
ax.fill(angles, values, color=ACCENT, alpha=0.4)

ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels, color=TEXT, fontsize=11)
ax.set_yticklabels([])
ax.spines["polar"].set_color(GRID)

plt.savefig("activity-radar.svg", format="svg", facecolor=BG)
plt.close()
