import requests
import os
import json

# Cargar variables desde el entorno del sistema
fortigate_url = os.getenv("FORTIGATE_URL")
fortigate_token = os.getenv("FORTIGATE_API_TOKEN")

if not fortigate_url or not fortigate_token:
    print("Error: Las variables de entorno FORTIGATE_URL y/o FORTIGATE_API_TOKEN no están configuradas.")
    exit(1)

response = requests.get(
    f"{fortigate_url}/monitor/vpn/ipsec",
    headers={"Authorization": f"Bearer {fortigate_token}"},
    verify=False,
)

if response.status_code == 200:
    with open("last_vpns.json", "w") as f:
        json.dump(response.json(), f)
    print("Datos obtenidos y guardados en 'last_vpns.json'.")
else:
    print(f"Error: {response.status_code} - {response.text}")
    exit(1)
