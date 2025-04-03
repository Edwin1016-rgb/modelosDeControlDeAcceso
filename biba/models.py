from acl import users, files

def has_permission(user, file, action):
    """Verifica si el usuario tiene permiso para realizar una acción sobre un archivo."""
    if user not in users or file not in files:
        return False
    
    user_level = users[user]
    file_level = files[file]
    
    # Regla de Biba: No leer hacia abajo, no escribir hacia arriba
    if action == "read":
        return user_level <= file_level  # Puede leer si su nivel es mayor o igual al del archivo
    elif action == "write":
        return user_level >= file_level  # Puede escribir si su nivel es menor o igual al del archivo
    
    return False
