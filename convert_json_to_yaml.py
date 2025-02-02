import json
import yaml

# Archivos de entrada y salida
input_file = "previous_vpns.json"  # Archivo JSON generado previamente
output_file = "previous_vpns.yml"  # Archivo YAML de salida

# Leer el archivo JSON
with open(input_file, "r") as f:
    data = json.load(f)

# Escribir el contenido en formato YAML
with open(output_file, "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print(f"Archivo convertido y guardado en {output_file}")
