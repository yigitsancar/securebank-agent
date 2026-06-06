import os

BASE_DIR = os.path.expanduser("~/securebank-devops-platform")

REPOS = {
    "backend": f"{BASE_DIR}/securebank",
    "frontend": f"{BASE_DIR}/securebank-frontend",
    "k8s": f"{BASE_DIR}/securebank-k8s",
}

EC2_HOST = "51.21.210.17"
EC2_USER = "ubuntu"
SSH_KEY = os.path.expanduser("~/.ssh/securebank-key.pem")
K8S_NAMESPACE = "securebank"

GITHUB_OWNER = "yigitsancar"

GITHUB_REPOS = {
    "backend": "securebank-devops-platform",
    "frontend": "securebank-frontend",
    "agent": "securebank-agent",
}
