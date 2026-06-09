from rich.console import Console
from rich.panel import Panel

from commands.db_commands import db_status
from commands.ops_commands import pods_status, svc_status, pvc_status, monitoring_status, restart_component
from commands.deploy_commands import deploy
from commands.pipeline_commands import pipeline_status
from commands.health_commands import health_status
from commands.git_commands import show_git_status, update_repo
from commands.project_commands import project_check
from commands.k8s_commands import k8s_status

console = Console()


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]SecureBank Agent v2[/bold cyan]\n"
            "Modüler DevOps yardımcı agent",
            border_style="cyan"
        )
    )


def help_menu():
    console.print("""
[bold green]Komutlar[/bold green]

status      Git + proje + Kubernetes durumunu gösterir
deploy      Git push sonrası pipeline durumunu gösterir
health      Frontend, backend, Grafana ve Prometheus erişimini kontrol eder
pipeline    GitHub Actions son çalışma durumunu gösterir
git         Sadece repository durumlarını gösterir
proje       Proje dosya kontrollerini gösterir
db          PostgreSQL kullanıcı ve işlem istatistiklerini gösterir
pods        Kubernetes pod durumlarını gösterir
svc         Kubernetes service durumlarını gösterir
pvc         PostgreSQL kalıcı disk durumunu gösterir
monitoring  Prometheus, Grafana ve target durumunu gösterir
restart     Seçilen Kubernetes deployment'ını restart eder
k8s         Kubernetes pod durumlarını gösterir
guncelle    Seçilen repository için git add/commit/push yapar
yardim      Komutları gösterir
cikis       Agent'tan çıkar
""")


def main():
    show_banner()
    help_menu()

    while True:
        command = input("\nsecurebank-agent > ").strip().lower()

        if command == "status":
            show_git_status()
            project_check()
            k8s_status()
        elif command == "deploy":
            deploy()
        elif command == "health":
            health_status()
        elif command == "pipeline":
            pipeline_status()
        elif command == "git":
            show_git_status()
        elif command == "proje":
            project_check()
        elif command == "db":
            db_status()
        elif command == "k8s":
            k8s_status()
        elif command == "pods":
            pods_status()
        elif command == "svc":
            svc_status()
        elif command == "pvc":
            pvc_status()
        elif command == "monitoring":
            monitoring_status()
        elif command.startswith("restart"):
            parts = command.split()
            if len(parts) != 2:
                console.print("[yellow]Kullanım: restart backend | restart frontend | restart postgres[/yellow]")
            else:
                restart_component(parts[1])
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
