import time
from rich.console import Console

from commands.git_commands import update_repo
from commands.pipeline_commands import pipeline_status_for_component

console = Console()


def select_component():
    console.print("[bold]Hangi bileşen deploy edilsin?[/bold]")
    console.print("1 - backend")
    console.print("2 - frontend")
    console.print("3 - k8s")

    choice = input("Seçim: ").strip()

    mapping = {
        "1": "backend",
        "2": "frontend",
        "3": "k8s",
    }

    return mapping.get(choice)


def deploy():
    console.print("\n[bold cyan]SecureBank Deploy Assistant v2[/bold cyan]")

    component = select_component()

    if not component:
        console.print("[red]Geçersiz seçim.[/red]")
        return

    console.print(f"\n[yellow]1.[/yellow] {component} için git işlemleri başlatılıyor...")

    update_repo(selected_repo=component)

    console.print("\n[yellow]2.[/yellow] Pipeline başlatılması bekleniyor...")
    time.sleep(15)

    console.print("\n[yellow]3.[/yellow] Pipeline takip ediliyor...")

    for attempt in range(12):
        result = pipeline_status_for_component(component)

        status = result["status"]
        conclusion = result["conclusion"]
        url = result["url"]

        console.print(f"[cyan]Kontrol {attempt + 1}/12[/cyan] -> status={status}, conclusion={conclusion}")

        if status == "completed":
            if conclusion == "success":
                console.print("[green]Pipeline başarıyla tamamlandı.[/green]")
            elif conclusion == "failure":
                console.print("[red]Pipeline başarısız oldu.[/red]")
            else:
                console.print(f"[yellow]Pipeline tamamlandı: {conclusion}[/yellow]")

            console.print(f"Pipeline URL: {url}")
            return

        time.sleep(10)

    console.print("[yellow]Pipeline hâlâ devam ediyor olabilir. Daha sonra 'pipeline' komutuyla tekrar kontrol et.[/yellow]")
