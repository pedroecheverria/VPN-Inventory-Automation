# TunnelVPN Automation 🚀  
Automatización del inventario de túneles VPN en **FortiGate** utilizando **Python, Ansible y NetBox**.  
Este sistema permite **crear, modificar, actualizar y eliminar** VPNs de manera automatizada, asegurando un inventario siempre actualizado.  

---

## 📌 POST (Creación de VPNs en NetBox)  
1️⃣ **Ejecutar `get_vpns.py`** → Consulta FortiGate y genera `last_vpns.json` (datos crudos).  
2️⃣ **Ejecutar `parse_v5.py`** → Extrae solo los elementos necesarios y genera `previous_vpns.json`.  
3️⃣ **Ejecutar `convert_json_to_yaml.py`** → Convierte el JSON en YAML.  
4️⃣ **Ejecutar `post_v4.yml`** → Playbook de Ansible para crear las VPNs en NetBox.  

---

## 🔄 PATCH (Actualización de VPNs en NetBox)  
🔹 **Si hay un orquestador corriendo, no hace falta ejecutar nuevamente los pasos anteriores.**  

1️⃣ **Ejecutar `get_netbox_vpns.yml`** → Obtiene VPNs existentes en NetBox y genera `patch_vpns.json`.  
2️⃣ **Ejecutar `sincro_v2.py`** → Compara VPNs de FortiGate con NetBox, generando `consolidated_vpns.json`.  
3️⃣ **Ejecutar `differences_for_patch.py`** → Genera `update_vpns.json` con cambios detectados.  
4️⃣ **Ejecutar `ansible-playbook patch.yml`** → Aplica los cambios en NetBox.  

---

## 🗑 DELETE (Eliminación de VPNs en NetBox)  
🔹 **Si hay un orquestador, los primeros pasos ya están ejecutados automáticamente.**  

1️⃣ **Ejecutar `delete_vpn.py`** → Compara `consolidated_vpns.json` con `patch_vpns.json` y genera `delete_vpns.json`.  
2️⃣ **Ejecutar `ansible-playbook delete.yml`** → Elimina en NetBox las VPNs que ya no existen en FortiGate.  

---

## ⏳ Orquestador  
Este flujo se puede ejecutar **cada 20 minutos** con un orquestador, asegurando que NetBox esté siempre sincronizado con FortiGate.  

---

📌 **Contribuciones:**  
Si deseas mejorar esta automatización, ¡siéntete libre de hacer un fork y enviar un PR!  

📌 **Contacto:**  
🔹 **Autor:** [Pedro Echeverria](https://github.com/pedroecheverria)  
🔹 **Repositorio:** [TunnelVPN Automation](https://github.com/pedroecheverria/TunnelVPN-automation.git)  
