from rich.console import Console

from commands.git_commands import update_repo
from commands.pipeline_commands import pipeline_status

console = Console()


def deploy():
    console.print(
        "\n[bold cyan]SecureBank Deploy Assistant[/bold cyan]"
    )

    console.print(
        "[yellow]1.[/yellow] Git işlemleri başlatılıyor..."
    )

    update_repo()

    console.print(
        "\n[yellow]2.[/yellow] Pipeline durumu kontrol ediliyor..."
    )

    pipeline_status()
