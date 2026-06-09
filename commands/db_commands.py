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


def query_db(sql):
    remote_cmd = (
        f"kubectl exec -n {K8S_NAMESPACE} deploy/postgres -- "
        f"psql -U postgres -d securebankdb -t -A -c \\\"{sql}\\\""
    )

    code, out, err = ssh_command(remote_cmd)

    if code != 0:
        return None, err

    return out.strip(), None


def db_status():
    table = Table(title="SecureBank Database Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    users, users_err = query_db("SELECT COUNT(*) FROM users;")
    admins, admins_err = query_db("SELECT COUNT(*) FROM users WHERE role = 'ADMIN';")
    transactions, transactions_err = query_db("SELECT COUNT(*) FROM transactions;")

    if users_err or admins_err or transactions_err:
        table.add_row("PostgreSQL", "[red]ERROR[/red]")
        table.add_row("Detail", users_err or admins_err or transactions_err)
    else:
        table.add_row("Users", users)
        table.add_row("Admins", admins)
        table.add_row("Transactions", transactions)
        table.add_row("PostgreSQL", "[green]UP[/green]")

    console.print(table)
