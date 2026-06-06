import json
import os
import urllib.request
from rich.console import Console
from rich.table import Table

from config import GITHUB_OWNER, GITHUB_REPOS

console = Console()


def fetch_latest_run(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo_name}/actions/runs?per_page=1"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "securebank-agent"
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        runs = data.get("workflow_runs", [])

        if not runs:
            return {
                "status": "NO_RUN",
                "conclusion": "-",
                "name": "-",
                "branch": "-",
                "url": "-"
            }

        latest = runs[0]

        return {
            "status": latest.get("status", "-"),
            "conclusion": latest.get("conclusion") or "-",
            "name": latest.get("name", "-"),
            "branch": latest.get("head_branch", "-"),
            "url": latest.get("html_url", "-")
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "conclusion": str(e),
            "name": "-",
            "branch": "-",
            "url": "-"
        }


def pipeline_status():
    table = Table(title="SecureBank GitHub Actions Pipeline Durumu")
    table.add_column("Bileşen", style="cyan")
    table.add_column("Repo")
    table.add_column("Workflow")
    table.add_column("Branch")
    table.add_column("Status")
    table.add_column("Conclusion")

    for component, repo_name in GITHUB_REPOS.items():
        result = fetch_latest_run(repo_name)

        status = result["status"]
        conclusion = result["conclusion"]

        if conclusion == "success":
            conclusion_text = "[green]success[/green]"
        elif conclusion == "failure":
            conclusion_text = "[red]failure[/red]"
        elif status == "in_progress":
            conclusion_text = "[yellow]running[/yellow]"
        else:
            conclusion_text = conclusion

        table.add_row(
            component,
            repo_name,
            result["name"],
            result["branch"],
            status,
            conclusion_text
        )

def pipeline_status_for_component(component):
    repo_name = GITHUB_REPOS.get(component)

    if not repo_name:
        return {
            "status": "ERROR",
            "conclusion": f"Unknown component: {component}",
            "name": "-",
            "branch": "-",
            "url": "-"
        }

    return fetch_latest_run(repo_name)

    console.print(table)
