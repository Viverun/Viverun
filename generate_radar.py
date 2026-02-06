import os
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# ================= CONFIG =================
USERNAME = "Viverun"   # your GitHub username
DAYS = 90              # contribution window

BG = "#0d1117"
GRID = "#30363d"
TEXT = "#c9d1d9"
ACCENT = "#2ea043"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

# ================= GRAPHQL QUERY =================
since = (datetime.utcnow() - timedelta(days=DAYS)).isoformat() + "Z"

query = """
query($user: String!, $since: DateTime!) {
  user(login: $user) {
    contributionsCollection(from: $since) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
"""

response = requests.post(
    "https://api.github.com/graphql",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    },
    json={
        "query": query,
        "variables": {
            "user": USERNAME,
            "since": since
        }
    }
)

data = response.json()

if "errors" in data:
    raise RuntimeError(data["errors"])

c = data["data"]["user"]["contributionsCollection"]

raw = {
    "Commits": c["totalCommitContributions"],
    "Code Review": c["totalPullRequestReviewContributions"],
    "Pull Requests": c["totalPullRequestContributions"],
    "Issues": c["totalIssueContributions"],
}

# prevent empty chart
total = sum(raw.values()) or 1
labels = list(raw.keys())
values = [round(v / total * 100, 1) for v in raw.values()]

# ================= RADAR CHART =================
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
angles = np.concatenate([angles, angles[:1]])
values = values + values[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.plot(angles, values, color=ACCENT, linewidth=2)
ax.fill(angles, values, color=ACCENT, alpha=0.25)

ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels, color=TEXT, fontsize=11)
ax.tick_params(pad=12)
ax.set_yticklabels([])
ax.spines["polar"].set_color(GRID)

ax.set_title(
    f"Contribution Breakdown (Last {DAYS} Days)",
    color=TEXT,
    pad=20,
    fontsize=13
)

plt.savefig("activity-radar.svg", format="svg", facecolor=BG)
plt.close()
