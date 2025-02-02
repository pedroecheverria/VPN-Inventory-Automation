import json
import os
import ipaddress

# Archivos
new_vpns_file = "last_vpns.json"  # Archivo generado por el GET
previous_vpns_file = "previous_vpns.json"  # Estado anterior de las VPNs

def convert_to_cidr(subnet):
    """Convierte una subred en formato 'IP/máscara' a formato CIDR."""
    try:
        ip, mask = subnet.split("/")
        return str(ipaddress.IPv4Network(f"{ip}/{mask}", strict=False))
    except ValueError:
        return subnet  # Devuelve la subred original si hay un error

def format_comment(comment):
    """Formatea los comentarios para que cada parte esté precedida por una viñeta."""
    if comment:
        return comment.replace(",", " -").strip()
    return ""

def parse_vpn_data(vpn_data):
    """Parsea los datos de las VPNs y los convierte al formato requerido."""
    parsed_results = []
    for vpn in vpn_data.get("results", []):
        proxyid = vpn.get("proxyid", [])
        # Validar si proxyid tiene al menos un elemento
        status = proxyid[0].get("status") if proxyid and isinstance(proxyid, list) else "unknown"
        
        parsed_vpn = {
            "name": vpn.get("name"),
            "status": status,
            # Limpia y formatea los comentarios con viñetas
            "comment": format_comment(vpn.get("comments", "").strip()),
            "remote_gateway": vpn.get("rgwy"),
            "tun_id": vpn.get("tun_id"),
            # Convertir subredes a formato amigable (lista separada por comas)
            "local_subnets": ", ".join([
                convert_to_cidr(src.get("subnet")) for proxy in vpn.get("proxyid", [])
                for src in proxy.get("proxy_src", [])
            ]),
            "remote_subnets": ", ".join([
                convert_to_cidr(dst.get("subnet")) for proxy in vpn.get("proxyid", [])
                for dst in proxy.get("proxy_dst", [])
            ])
        }
        parsed_results.append(parsed_vpn)
    return {"results": parsed_results}

# Carga el estado previo
if os.path.exists(previous_vpns_file):
    with open(previous_vpns_file, "r") as f:
        previous_vpns = json.load(f)
else:
    previous_vpns = {"results": []}

# Carga el estado actual
with open(new_vpns_file, "r") as f:
    try:
        raw_data = json.load(f)
    except json.JSONDecodeError:
        print("Error: El archivo 'last_vpns.json' tiene un formato inválido.")
        exit(1)

# Parseo del estado actual
new_vpns = parse_vpn_data(raw_data)

# Encuentra diferencias
differences = [vpn for vpn in new_vpns.get("results", []) if vpn not in previous_vpns.get("results", [])]

# Imprime los cambios detectados
if differences:
    print("Cambios detectados en las configuraciones de VPN:")
    for change in differences:
        print(json.dumps(change, indent=4))  # Imprime cada cambio en formato JSON legible
else:
    print("No hay diferencias detectadas.")

# Actualiza el archivo previo con el estado actual
with open(previous_vpns_file, "w") as f:
    json.dump(new_vpns, f, indent=4)
print(f"El archivo '{previous_vpns_file}' se ha actualizado con el estado actual.")
