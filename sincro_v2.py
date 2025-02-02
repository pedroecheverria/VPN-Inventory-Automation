import json

# Archivos
previous_vpns_file = "previous_vpns.json"  # VPNs más recientes parseadas
consolidated_vpns_file = "consolidated_vpns.json"  # Archivo consolidado existente
patch_vpns_file = "patch_vpns.json"  # VPNs actuales desde NetBox (crudo del GET)

# Cargar archivos
with open(previous_vpns_file, "r") as f:
    previous_vpns = json.load(f)

try:
    with open(consolidated_vpns_file, "r") as f:
        consolidated_vpns = json.load(f)
except FileNotFoundError:
    consolidated_vpns = {"results": []}  # Si no existe, inicializamos un archivo vacío

try:
    with open(patch_vpns_file, "r") as f:
        patch_vpns = json.load(f)
except FileNotFoundError:
    print("⚠️ Archivo 'patch_vpns.json' no encontrado. Asegúrate de ejecutarlo antes.")
    exit()

# Crear mapeo de VPNs en patch_vpns.json por nombre
patch_vpn_map = {vpn["name"]: vpn for vpn in patch_vpns["results"]}

# Crear nuevo consolidado
updated_consolidated = {"results": []}

for vpn in previous_vpns["results"]:
    # Buscar la VPN correspondiente en patch_vpns.json por nombre
    matching_patch_vpn = patch_vpn_map.get(vpn["name"])

    if matching_patch_vpn:
        # Agregar campos id y Netbox_ID desde patch_vpns.json
        vpn["Netbox_ID"] = matching_patch_vpn["custom_fields"].get("Netbox_ID")
        vpn["id"] = matching_patch_vpn.get("id")
    else:
        # Mostrar advertencia si no se encuentra en patch_vpns.json
        print(f"⚠️ VPN '{vpn['name']}' no encontrada en 'patch_vpns.json'. No se incluirán campos 'id' o 'Netbox_ID'.")

    # Agregar al nuevo consolidado
    updated_consolidated["results"].append(vpn)

# Guardar el archivo consolidado actualizado
with open(consolidated_vpns_file, "w") as f:
    json.dump(updated_consolidated, f, indent=4)

print(f"Archivo consolidado actualizado: {consolidated_vpns_file}")
