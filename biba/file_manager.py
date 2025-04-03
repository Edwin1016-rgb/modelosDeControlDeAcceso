import json
import os

JSON_PATH = "biba/files/data.json"

def load_data():
    """Carga los datos desde el archivo JSON."""
    if not os.path.exists(JSON_PATH):
        return {}
    
    with open(JSON_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    """Guarda los datos en el archivo JSON."""
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

def read_user_section(file_name, user):
    """Lee solo la sección del usuario en el JSON."""
    print(f"Buscando archivo: '{file_name}', usuario: '{user}'") 
    data = load_data()
    return data.get(file_name, {}).get(user, "(vacio)") 

def write_user_section(file_name, user, new_content):
    """Escribe en la sección del usuario dentro del JSON sin afectar otras secciones."""
    data = load_data()
    
    if file_name not in data:
        data[file_name] = {}

    data[file_name][user] = new_content  # Modifica solo la parte del usuario
    
    save_data(data)
    return "[OK] Contenido guardado correctamente."

# Funciones para la GUI
def read_file_for_gui(file_name, user):
    return read_user_section(file_name, user)

def write_file_from_gui(file_name, user, content):
    return write_user_section(file_name, user, content)

# Prueba básica
if __name__ == "__main__":
    archivo = "confidential.txt"
    usuario = "Empleado"
    nuevo_texto = "Información actualizada del Empleado."

    print(read_file_for_gui(archivo, usuario))
    print(write_file_from_gui(archivo, usuario, nuevo_texto))
