from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import subprocess
import os

console = Console()

BASE_DIR = os.path.expanduser("~/securebank-devops-platform")

REPOS = {
    "backend": f"{BASE_DIR}/securebank",
    "frontend": f"{BASE_DIR}/securebank-frontend",
    "k8s": f"{BASE_DIR}/securebank-k8s",
}


def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]SecureBank Agent v1[/bold cyan]\n"
            "Projeye özel DevOps yardımcı agent",
            border_style="cyan"
        )
    )


def help_menu():
    console.print("""
[bold green]Komutlar[/bold green]

status      Proje repository durumlarını gösterir
guncelle    Seçilen repository için git add/commit/push yapar
yardim      Komutları gösterir
cikis       Agent'tan çıkar
""")

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

def status():
    table = Table(title="SecureBank Repository Durumu")
    table.add_column("Repo", style="cyan")
    table.add_column("Branch")
    table.add_column("Durum")

    for name, path in REPOS.items():
        code_branch, branch, _ = run_command("git branch --show-current", cwd=path)
        code_status, output, err = run_command("git status --short", cwd=path)

        if code_status != 0:
            durum = f"[red]Hata: {err}[/red]"
        elif output:
            changed_count = len(output.splitlines())
            durum = f"[yellow]{changed_count} değişiklik var[/yellow]"
        else:
            durum = "[green]Temiz[/green]"

        table.add_row(name, branch if branch else "-", durum)

    console.print(table)
    project_check()

def update_repo():
    console.print("[bold]Hangi repository güncellensin?[/bold]")
    console.print("1 - backend")
    console.print("2 - frontend")
    console.print("3 - k8s")

    choice = input("Seçim: ").strip()

    mapping = {
        "1": "backend",
        "2": "frontend",
        "3": "k8s"
    }

    repo_name = mapping.get(choice)

    if not repo_name:
        console.print("[red]Geçersiz seçim.[/red]")
        return

    path = REPOS[repo_name]

    code, changes, err = run_command("git status --short", cwd=path)

    if code != 0:
        console.print(f"[red]Git status hatası:[/red] {err}")
        return

    if not changes:
        console.print("[green]Değişiklik yok. Commit atılmadı.[/green]")
        return

    console.print(f"\n[bold yellow]{repo_name} içinde değişiklikler:[/bold yellow]")
    console.print(changes)

    commit_message = input("\nCommit mesajı: ").strip()

    if not commit_message:
        console.print("[red]Commit mesajı boş olamaz.[/red]")
        return

    console.print("\n[cyan]Git add çalışıyor...[/cyan]")
    run_command("git add .", cwd=path)

    console.print("[cyan]Git commit çalışıyor...[/cyan]")
    code, out, err = run_command(f'git commit -m "{commit_message}"', cwd=path)

    if code != 0:
        console.print(f"[red]Commit başarısız:[/red]\n{err}")
        return

    console.print(out)

    console.print("[cyan]Git push çalışıyor...[/cyan]")
    code, out, err = run_command("git push", cwd=path)

    if code != 0:
        console.print(f"[red]Push başarısız:[/red]\n{err}")
        return

    console.print("[green]Başarıyla GitHub'a gönderildi.[/green]")


def main():
    show_banner()
    help_menu()

    while True:
        command = input("\nsecurebank-agent > ").strip().lower()

        if command == "status":
            status()
        elif command == "guncelle":
            update_repo()
        elif command == "yardim":
            help_menu()
        elif command == "cikis":
            console.print("[cyan]Agent kapatılıyor...[/cyan]")
            break
        else:
            console.print("[red]Bilinmeyen komut. 'yardim' yazabilirsin.[/red]")


if __name__ == "__main__":
    main()
