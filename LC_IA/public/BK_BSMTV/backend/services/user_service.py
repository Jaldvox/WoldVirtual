def get_user_by_id(user_id):
    # Simula la obtención de un usuario por ID
    users = get_all_users()
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def create_user(user_data):
    # Simula la creación de un nuevo usuario
    users = get_all_users()
    new_id = max(user['id'] for user in users) + 1
    user_data['id'] = new_id
    users.append(user_data)
    return user_data

def update_user(user_id, user_data):
    # Simula la actualización de un usuario existente
    users = get_all_users()
    for user in users:
        if user['id'] == user_id:
            user.update(user_data)
            return user
    return None

def delete_user(user_id):
    # Simula la eliminación de un usuario
    users = get_all_users()
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return True
    return False

def get_all_users():
    # Simula una lista de usuarios
    return [
        {'id': 1, 'name': 'Juan', 'email': 'juan@example.com'},
        {'id': 2, 'name': 'Maria', 'email': 'maria@example.com'},
    ]