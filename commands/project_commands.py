import os
from rich.console import Console
from rich.table import Table

from config import REPOS

console = Console()


def project_check():
    table = Table(title="SecureBank Proje Kontrolü")
    table.add_column("Bileşen", style="cyan")
    table.add_column("Kontrol")
    table.add_column("Durum")

    checks = [
        ("Backend", "build.gradle", f"{REPOS['backend']}/build.gradle"),
        ("Frontend", "package.json", f"{REPOS['frontend']}/package.json"),
        ("Kubernetes", "namespace.yaml", f"{REPOS['k8s']}/namespace.yaml"),
        ("Kubernetes", "backend.yaml", f"{REPOS['k8s']}/backend.yaml"),
        ("Kubernetes", "frontend.yaml", f"{REPOS['k8s']}/frontend.yaml"),
        ("Kubernetes", "postgres.yaml", f"{REPOS['k8s']}/postgres.yaml"),
    ]

    for component, check_name, path in checks:
        if os.path.exists(path):
            table.add_row(component, check_name, "[green]Var[/green]")
        else:
            table.add_row(component, check_name, "[red]Yok[/red]")

    console.print(table)
