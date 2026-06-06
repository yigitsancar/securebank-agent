from rich.console import Console
from rich.table import Table

from config import REPOS
from utils.shell import run_command

console = Console()


def show_git_status():
    table = Table(title="SecureBank Repository Durumu")
    table.add_column("Repo", style="cyan")
    table.add_column("Branch")
    table.add_column("Durum")

    for name, path in REPOS.items():
        _, branch, _ = run_command("git branch --show-current", cwd=path)
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


def update_repo():
    console.print("[bold]Hangi repository güncellensin?[/bold]")
    console.print("1 - backend")
    console.print("2 - frontend")
    console.print("3 - k8s")

    choice = input("Seçim: ").strip()

    mapping = {
        "1": "backend",
        "2": "frontend",
        "3": "k8s",
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
