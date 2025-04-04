# Usuarios y niveles
users = {
    'Admin': 3,
    'Empleado': 2,
    'Visitante': 1
}

# Archivos y niveles
files = {
    'top_secret.txt': 3,
    'confidential.txt': 2,
    'public.txt': 1
}

# Listas de Control de Acceso (ACLs)
acl = {
    'top_secret.txt': {  # Nivel 3
        'Admin': ['read', 'write'],
        'Empleado': ['read'],  
        'Visitante': ['read']  
    },
    'confidential.txt': {  # Nivel 2
        'Admin': ['write'],  
        'Empleado': ['read', 'write'],  
        'Visitante': ['read']  
    },
    'public.txt': {  # Nivel 1
        'Admin': ['write'],  
        'Empleado': ['write'],  
        'Visitante': ['read', 'write']
    }
}
