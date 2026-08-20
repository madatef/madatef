"""Generate banner-light.svg, banner-dark.svg, and stats.svg from the GitHub API.

Reads ACCESS_TOKEN (a PAT with `repo` scope for private-repo visibility) and
USER_NAME from the environment. Writes both SVG variants to the repo root.
"""

import datetime
import os
import time

import requests

TOKEN = os.environ["ACCESS_TOKEN"]
USER = os.environ["USER_NAME"]
HEADERS = {"Authorization": f"token {TOKEN}"}
GQL = "https://api.github.com/graphql"

NAME = "Mohammad Atef"
TAGLINE = "applied AI engineer  ·  agents, retrieval, and the systems around them"
SUBLINE = "Cairo, Egypt"


def graphql(query, variables):
    for attempt in range(5):
        r = requests.post(GQL, json={"query": query, "variables": variables}, headers=HEADERS)
        if r.status_code == 200:
            payload = r.json()
            if "errors" in payload:
                raise RuntimeError(payload["errors"])
            return payload["data"]
        if r.status_code in (403, 502):
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
    raise RuntimeError("GraphQL request failed after retries")


def account_created():
    q = "query($login:String!){ user(login:$login){ createdAt } }"
    stamp = graphql(q, {"login": USER})["user"]["createdAt"]
    return datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")


def commit_total(since):
    """Sum commit contributions year by year; the API caps each window at one year."""
    q = """
    query($login:String!,$from:DateTime!,$to:DateTime!){
      user(login:$login){
        contributionsCollection(from:$from,to:$to){
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }
    """
    total = 0
    start = since
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    while start < now:
        end = min(start + datetime.timedelta(days=365), now)
        c = graphql(q, {
            "login": USER,
            "from": start.isoformat() + "Z",
            "to": end.isoformat() + "Z",
        })["user"]["contributionsCollection"]
        total += c["totalCommitContributions"] + c["restrictedContributionsCount"]
        start = end
    return total


def repo_summary():
    """Return (repo_count, star_count, follower_count, [name_with_owner...])."""
    q = """
    query($login:String!,$cursor:String){
      user(login:$login){
        followers{ totalCount }
        repositories(first:100, after:$cursor, ownerAffiliations:[OWNER],
                     isFork:false, privacy:null){
          totalCount
          pageInfo{ hasNextPage endCursor }
          nodes{ nameWithOwner stargazerCount }
        }
      }
    }
    """
    cursor, names, stars = None, [], 0
    while True:
        u = graphql(q, {"login": USER, "cursor": cursor})["user"]
        repos = u["repositories"]
        for n in repos["nodes"]:
            names.append(n["nameWithOwner"])
            stars += n["stargazerCount"]
        if not repos["pageInfo"]["hasNextPage"]:
            return repos["totalCount"], stars, u["followers"]["totalCount"], names
        cursor = repos["pageInfo"]["endCursor"]


def lines_of_code(repo_names):
    """Sum your own additions and deletions across repos via the REST stats endpoint."""
    added = deleted = 0
    for full_name in repo_names:
        url = f"https://api.github.com/repos/{full_name}/stats/contributors"
        for _ in range(4):
            r = requests.get(url, headers=HEADERS)
            if r.status_code == 202:      # GitHub is computing the stats; retry
                time.sleep(3)
                continue
            break
        if r.status_code != 200 or not r.text.strip():
            continue
        for contributor in r.json():
            if contributor.get("author", {}).get("login", "").lower() != USER.lower():
                continue
            for week in contributor["weeks"]:
                added += week["a"]
                deleted += week["d"]
    return added, deleted


def uptime(created):
    days = (datetime.datetime.now() - created).days
    years, rem = divmod(days, 365)
    months = rem // 30
    return f"{years} yrs, {months} mos"


THEMES = {
    "light": {
        "band": "#0F566E", "name": "#E1EEF5", "sub": "#9FCBE1", "meta": "#5DA2CA",
        "stat": "#5F5E5A",
    },
    "dark": {
        "band": "#042234", "name": "#E1EEF5", "sub": "#5DA2CA", "meta": "#1D669E",
        "stat": "#8b949e",
    },
}


def render_banner(theme_name):
    """Static header band. Regenerated alongside stats so both themes stay in sync."""
    t = THEMES[theme_name]
    width, height = 840, 108
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{NAME} — {SUBLINE}">
<rect width="{width}" height="{height}" rx="10" fill="{t["band"]}"/>
<text x="34" y="46" font-family="-apple-system,Segoe UI,Helvetica,sans-serif" font-size="26" font-weight="500" fill="{t["name"]}">{NAME}</text>
<text x="34" y="72" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" fill="{t["sub"]}">{TAGLINE}</text>
<text x="34" y="92" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" fill="{t["meta"]}">{SUBLINE}</text>
</svg>'''


def render_stats(parts):
    """One quiet monospace line, theme-neutral via currentColor."""
    text = "   ·   ".join(parts)
    width = 12 + len(text) * 6.7
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="20" viewBox="0 0 {width:.0f} 20" role="img" aria-label="{text}">
<text x="0" y="14" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11" fill="#8b949e">{text}</text>
</svg>'''


def main():
    created = account_created()
    repos, stars, followers, names = repo_summary()
    commits = commit_total(created)
    added, deleted = lines_of_code(names)

    parts = [
        f"{commits:,} commits",
        f"{added + deleted:,} lines written",
        f"{repos} repositories",
        f"active {uptime(created)}",
        "refreshed daily",
    ]

    for theme in THEMES:
        with open(f"banner-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(render_banner(theme))
    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write(render_stats(parts))
    print(f"commits={commits} loc={added + deleted} repos={repos}")


if __name__ == "__main__":
    main()
