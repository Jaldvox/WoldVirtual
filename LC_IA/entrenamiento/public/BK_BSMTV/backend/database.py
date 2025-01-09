def agregar_usuario(usuarios, usuario):
    usuarios.append(usuario)
    return usuarios

def eliminar_usuario(usuarios, usuario):
    if usuario in usuarios:
        usuarios.remove(usuario)
    return usuarios

def listar_usuarios(usuarios):
    return usuarios

# Simulación de una base de datos en memoria
usuarios = []

# Ejemplo de uso
if __name__ == "__main__":
    # Agregar usuarios
    agregar_usuario(usuarios, "usuario1")
    agregar_usuario(usuarios, "usuario2")
    
    # Listar usuarios
    print(listar_usuarios(usuarios))
    
    # Eliminar un usuario
    eliminar_usuario(usuarios, "usuario1")
    
    # Listar usuarios nuevamente
    print(listar_usuarios(usuarios))