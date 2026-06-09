from rich.console import Console
from rich.table import Table

from config import EC2_HOST, EC2_USER, SSH_KEY, K8S_NAMESPACE
from utils.shell import run_command

console = Console()


def ssh_command(remote_command):
    command = (
        f'ssh -i {SSH_KEY} {EC2_USER}@{EC2_HOST} '
        f'"export KUBECONFIG=/home/ubuntu/.kube/config && {remote_command}"'
    )
    return run_command(command)


def pods_status():
    code, out, err = ssh_command(
        f"kubectl get pods -n {K8S_NAMESPACE} --no-headers"
    )

    if code != 0:
        console.print("[red]Pod durumu alınamadı.[/red]")
        console.print(err)
        return

    table = Table(title="SecureBank Pods")
    table.add_column("Pod", style="cyan")
    table.add_column("Ready")
    table.add_column("Status")
    table.add_column("Restarts")
    table.add_column("Age")

    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 5:
            table.add_row(parts[0], parts[1], parts[2], " ".join(parts[3:-1]), parts[-1])

    console.print(table)


def svc_status():
    code, out, err = ssh_command(
        f"kubectl get svc -n {K8S_NAMESPACE} --no-headers"
    )

    if code != 0:
        console.print("[red]Service durumu alınamadı.[/red]")
        console.print(err)
        return

    table = Table(title="SecureBank Services")
    table.add_column("Name", style="cyan")
    table.add_column("Type")
    table.add_column("Cluster IP")
    table.add_column("External IP")
    table.add_column("Ports")
    table.add_column("Age")

    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 6:
            table.add_row(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])

    console.print(table)


def pvc_status():
    code, out, err = ssh_command(
        f"kubectl get pvc -n {K8S_NAMESPACE} --no-headers"
    )

    if code != 0:
        console.print("[red]PVC durumu alınamadı.[/red]")
        console.print(err)
        return

    table = Table(title="SecureBank Persistent Volumes")
    table.add_column("Name", style="cyan")
    table.add_column("Status")
    table.add_column("Volume")
    table.add_column("Capacity")
    table.add_column("Access Modes")
    table.add_column("Storage Class")
    table.add_column("Age")

    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 7:
            table.add_row(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[-1])

    console.print(table)


def monitoring_status():
    checks = [
        ("Prometheus", f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 5 http://localhost:9090/-/healthy"),
        ("Grafana", f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 5 http://localhost:3000/login"),
        ("Prometheus Target", "curl -s http://localhost:9090/api/v1/targets | grep -q 'health.*up' && echo UP || echo DOWN"),
    ]

    table = Table(title="SecureBank Monitoring")
    table.add_column("Bileşen", style="cyan")
    table.add_column("Durum")
    table.add_column("Detay")

    for name, remote_cmd in checks:
        code, out, err = ssh_command(remote_cmd)

        if code == 0 and (out in ["200", "302", "UP"]):
            table.add_row(name, "[green]UP[/green]", out)
        else:
            table.add_row(name, "[red]DOWN[/red]", err or out)

    console.print(table)


def restart_component(component):
    mapping = {
        "backend": "securebank-backend",
        "frontend": "securebank-frontend",
        "postgres": "postgres",
    }

    deployment = mapping.get(component)

    if not deployment:
        console.print("[red]Geçersiz bileşen. backend, frontend veya postgres yaz.[/red]")
        return

    console.print(f"[yellow]{component} deployment restart ediliyor...[/yellow]")

    code, out, err = ssh_command(
        f"kubectl rollout restart deployment/{deployment} -n {K8S_NAMESPACE} && "
        f"kubectl rollout status deployment/{deployment} -n {K8S_NAMESPACE}"
    )

    if code != 0:
        console.print("[red]Restart başarısız.[/red]")
        console.print(err)
        return

    console.print("[green]Restart tamamlandı.[/green]")
    console.print(out)

