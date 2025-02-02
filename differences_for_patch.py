import json

# Archivos
patch_vpns_file = "patch_vpns.json"  # VPNs obtenidas desde NetBox en crudo
consolidated_vpns_file = "consolidated_vpns.json"  # VPNs con Netbox_ID del previous_vpn.json para no sobreescribir en este.
update_vpns_file = "update_vpns.json"  # Archivo parseado que tiene su netbob_id y se usa de salida para el PATCH

# Cargar archivos
with open(patch_vpns_file, "r") as f:
    patch_vpns = json.load(f)

with open(consolidated_vpns_file, "r") as f:
    consolidated_vpns = json.load(f)

# Crear mapeo de VPNs consolidadas por Netbox_ID
consolidated_vpn_map = {vpn["Netbox_ID"]: vpn for vpn in consolidated_vpns["results"]}

# Detectar cambios
updates = []
for patch_vpn in patch_vpns["results"]:
    netbox_id = patch_vpn["custom_fields"].get("Netbox_ID")
    if netbox_id and netbox_id in consolidated_vpn_map:
        consolidated_vpn = consolidated_vpn_map[netbox_id]
        # Comparar configuraciones, ignorando el 'id' y otros campos que no queremos considerar
        fields_to_compare = ["name", "status", "remote_gateway", "local_subnets", "remote_subnets"]
        differences = any(
            consolidated_vpn.get(field) != patch_vpn.get(field)
            for field in fields_to_compare
        )
        if differences:
            updated_vpn = {
                "id": patch_vpn["id"],  # UUID interno de NetBox
                **consolidated_vpn  # Datos actualizados
            }
            updates.append(updated_vpn)

# Guardar actualizaciones
with open(update_vpns_file, "w") as f:
    json.dump({"results": updates}, f, indent=4)

print(f"Archivo '{update_vpns_file}' generado con las actualizaciones.")
