import json
import yaml

# Archivos de entrada y salida
json_file = "update_vpns.json"  # Archivo JSON de entrada
yaml_file = "update_vpns.yml"  # Archivo YAML de salida

def convert_json_to_yaml(json_file, yaml_file):
    """Convierte un archivo JSON a YAML."""
    try:
        # Leer datos del archivo JSON
        with open(json_file, "r") as jf:
            data = json.load(jf)

        # Escribir datos en formato YAML
        with open(yaml_file, "w") as yf:
            yaml.dump(data, yf, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"Archivo YAML generado exitosamente: {yaml_file}")

    except Exception as e:
        print(f"Error al convertir JSON a YAML: {e}")

# Ejecutar la conversión
convert_json_to_yaml(json_file, yaml_file)
