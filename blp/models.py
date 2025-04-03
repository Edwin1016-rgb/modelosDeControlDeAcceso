
# models.py
from acl import users, files, acl

def can_read(user, file):
    user_level = users[user]
    file_level = files[file]
    # Bell-LaPadula: No read up
    if user_level < file_level:
        print(f"[DENEGADO] {user} no puede leer archivos de nivel superior.")
        return False

    if 'read' in acl[file].get(user, []):
        return True
    else:
        print(f"[DENEGADO] {user} no tiene permiso de lectura en {file}.")
        return False

def can_write(user, file):
    user_level = users[user]
    file_level = files[file]

    # Bell-LaPadula: No write down
    if user_level >file_level:
        print(f"[DENEGADO] {user} no puede escribir en archivos de nivel inferior.")
        return False

    if 'write' in acl[file].get(user, []):
        return True
    else:
        print(f"[DENEGADO] {user} no tiene permiso de escritura en {file}.")
        return False
