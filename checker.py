#!/bin/python3
import shutil
import subprocess
import json
import os

HOME_DIR=str(os.getenv('HOME'))
NUGET_PASSWORD=str(os.getenv('PTM_NUGET_PASSWORD'))

# Check if executable exists
def check_command(command, description):
    if shutil.which(command):
        print(f"{description}: OK")
    else:
        print(f"{description}: Fail")

def cleanup():
  subprocess.run(
    ["rm", "-rf", "/tmp/ptm-tools"]
  )

# a dict of executable/description
exec_check_commands = {
    "git": "Git",
    "docker": "Docker",
    "gcloud": "Google Cloud CLI",
    "ptm-tools": "PTM-Tools CLI",
    "dbeaver": "DBeaver",
    "cloud-sql-proxy": "CloudSQL Proxy"
}

# a tuple with commands to check if env is setup
env_commands = [
  (
    ["gcloud", "auth", "list", "--format", "json"],
    "Login do gcloud",
    True
  ),
  (
    ["cat", HOME_DIR+"/.config/gcloud/application_default_credentials.json"],
    "GCloud ADC",
    False),
  (
    ["cat", HOME_DIR+"/.ssh/id_rsa.pub"],
    "Chave pública",
    False),
  (
    ["git", "clone", "--depth", "1", "git@github.com:PortalTelemedicina/ptm-tools", "/tmp/ptm-tools"],
    "Chave pública configurada no GitHub",
    False
  ),
  (
    ["grep", "ptm-iac-dev", HOME_DIR+"/.kube/config"],
    "Credenciais do cluster de desenvolvimento",
    False
  ),
  (
    ["curl", "-s", "--fail", "-u", "appsettings:"+NUGET_PASSWORD, "https://nuget.ptmdev.com.br/v3/index.json"],
    "Senha do servidor NUGET",
    False
  ),
  
]

# Function to run a command and check its output and exit code
def run_command(command, description, jsonOutputValidation):
    try:
        result = subprocess.run(
            command, 
            text=True, 
            capture_output=True, 
            check=False
        )
        if result.returncode == 0:
            if jsonOutputValidation:
                parsed_json = json.loads(result.stdout)
                len(parsed_json) > 0
            
            print(f"{description}: OK")
        else:
            print(f"{description}: Fail")
            if DEBUG:
              print(f"Error: {result.stderr.strip()}")
              print(f"Exit Code: {result.returncode}")
    except FileNotFoundError:
        print(f"{description}: Command not found")


print("=== Verificando executáveis disponíveis na máquina ===")
for cmd, desc in exec_check_commands.items():
    check_command(cmd, desc)
print("Feito!")  

print("\n=== Verificando configurações do ambiente ===")
for cmd, desc, validation in env_commands:
    run_command(cmd, desc, validation)
print("Feito!")  
    

print("\nAnálise finalizada!")
print("Limpando...")
cleanup()