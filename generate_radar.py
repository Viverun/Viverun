import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

# ================= CONFIG =================
USERNAME = "Viverun"          # your GitHub username
DAYS = 365                    # activity window
OUT_FILE = "activity-radar.svg"

BG = "#0d1117"
GRID = "#30363d"
TEXT = "#c9d1d9"
ACCENT = "#2ea043"

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

# ================= GRAPHQL =================
since = (datetime.now(timezone.utc) - timedelta(days=DAYS)).isoformat()

query = """
query($login: String!, $since: DateTime!) {
  user(login: $login) {

    contributionsCollection(from: $since) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }

  }
}
"""

resp = requests.post(
    "https://api.github.com/graphql",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={"query": query, "variables": {"login": USERNAME, "since": since}},
)

resp.raise_for_status()
data = resp.json()

c = data["data"]["user"]["contributionsCollection"]

raw = {
    "Commits": c["totalCommitContributions"],
    "Code Review": c["totalPullRequestReviewContributions"],
    "Pull Requests": c["totalPullRequestContributions"],
    "Issues": c["totalIssueContributions"],
}

print("Raw activity:", raw)

# ================= NORMALIZE (RADAR CORRECT WAY) =================
max_value = max(raw.values()) or 1
values = [v / max_value * 100 for v in raw.values()]

labels = list(raw.keys())

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
angles = np.concatenate([angles, angles[:1]])
values = values + values[:1]

# ================= PLOT =================
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.plot(angles, values, color=ACCENT, linewidth=2)
ax.fill(angles, values, color=ACCENT, alpha=0.4)

ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels, color=TEXT, fontsize=11)
ax.set_yticklabels([])
ax.spines["polar"].set_color(GRID)
ax.grid(color=GRID, linewidth=0.8)

plt.title("Contribution Breakdown", color=TEXT, pad=20)
plt.savefig(OUT_FILE, format="svg", facecolor=BG)
plt.close()

print(f"Saved {OUT_FILE}")
