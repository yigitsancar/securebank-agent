from rich.console import Console
from rich.table import Table

from config import EC2_HOST
from utils.shell import run_command

console = Console()


def check_url(name, url):
    command = f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 5 {url}"
    code, out, err = run_command(command)

    if code != 0:
        return name, url, "DOWN", err

    if out in ["200", "302"]:
        return name, url, "UP", out

    return name, url, "WARNING", out


def health_status():
    services = [
        ("Frontend", f"http://{EC2_HOST}:30080"),
        ("Backend Health", f"http://{EC2_HOST}:30081/actuator/health"),
        ("Grafana", f"http://{EC2_HOST}:3000"),
        ("Prometheus", f"http://{EC2_HOST}:9090"),
    ]

    table = Table(title="SecureBank Health Check")
    table.add_column("Servis", style="cyan")
    table.add_column("URL")
    table.add_column("Durum")
    table.add_column("Kod / Hata")

    for name, url in services:
        service_name, service_url, status, detail = check_url(name, url)

        if status == "UP":
            status_text = "[green]UP[/green]"
        elif status == "WARNING":
            status_text = "[yellow]WARNING[/yellow]"
        else:
            status_text = "[red]DOWN[/red]"

        table.add_row(service_name, service_url, status_text, detail)

    console.print(table)
