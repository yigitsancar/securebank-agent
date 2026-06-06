from rich.console import Console
from rich.table import Table

from config import EC2_HOST, EC2_USER, SSH_KEY, K8S_NAMESPACE
from utils.shell import run_command

console = Console()


def k8s_status():
    command = (
        f'ssh -i {SSH_KEY} {EC2_USER}@{EC2_HOST} '
        f'"KUBECONFIG=/home/ubuntu/.kube/config kubectl get pods -n {K8S_NAMESPACE} --no-headers"'
    )

    code, out, err = run_command(command)

    if code != 0:
        console.print("[red]Kubernetes durumu alınamadı.[/red]")
        console.print(err)
        return

    table = Table(title="SecureBank Kubernetes Pod Durumu")
    table.add_column("Pod", style="cyan")
    table.add_column("Ready")
    table.add_column("Status")
    table.add_column("Restarts")
    table.add_column("Age")

    for line in out.splitlines():
        parts = line.split()

        if len(parts) >= 5:
            pod_name = parts[0]
            ready = parts[1]
            status = parts[2]
            age = parts[-1]
            restarts = " ".join(parts[3:-1])

            table.add_row(
                pod_name,
                ready,
                status,
                restarts,
                age
            )

    console.print(table)
