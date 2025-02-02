import json

# Archivos
consolidated_vpns_file = "consolidated_vpns.json"  # Archivo consolidado
patch_vpns_file = "patch_vpns.json"  # Archivo crudo obtenido del GET de NetBox
delete_vpns_file = "delete_vpns.json"  # Salida con VPNs a eliminar

# Cargar archivos
with open(consolidated_vpns_file, "r") as f:
    consolidated_vpns = json.load(f)

with open(patch_vpns_file, "r") as f:
    patch_vpns = json.load(f)

# Crear conjuntos de Netbox_ID
consolidated_netbox_ids = {vpn["Netbox_ID"] for vpn in consolidated_vpns["results"]}
patch_netbox_ids = {vpn["custom_fields"]["Netbox_ID"] for vpn in patch_vpns["results"]}

# Identificar Netbox_IDs presentes en patch pero ausentes en consolidated
to_delete_ids = patch_netbox_ids - consolidated_netbox_ids

# Generar la lista de objetos a eliminar
to_delete_vpns = [
    {"id": vpn["id"], "Netbox_ID": vpn["custom_fields"]["Netbox_ID"], "name": vpn["name"]}
    for vpn in patch_vpns["results"]
    if vpn["custom_fields"]["Netbox_ID"] in to_delete_ids
]

# Guardar el archivo delete_vpns.json
with open(delete_vpns_file, "w") as f:
    json.dump({"results": to_delete_vpns}, f, indent=4)

print(f"Archivo de VPNs a eliminar generado: {delete_vpns_file}")
