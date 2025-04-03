
# acl.py

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
    'top_secret.txt': {
        'Admin': ['read', 'write'],
        'Empleado': [],
        'Visitante': []
    },
    'confidential.txt': {
        'Admin': ['read'],
        'Empleado': ['read', 'write'],
        'Visitante': []
    },
    'public.txt': {
        'Admin': ['read'],
        'Empleado': ['read'],
        'Visitante': ['read', 'write']
    }
}
