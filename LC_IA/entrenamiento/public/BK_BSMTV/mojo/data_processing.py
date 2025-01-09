def process_data(user_data):
    # Simula el procesamiento de datos de usuarios
    processed_data = []
    for user in user_data:
        # Aquí se pueden aplicar transformaciones o validaciones
        processed_data.append({
            'id': user['id'],
            'name': user['name'].strip().title(),
            'email': user['email'].lower()
        })
    return processed_data

def filter_users_by_name(user_data, name):
    # Filtra usuarios por nombre
    return [user for user in user_data if name.lower() in user['name'].lower()]

def sort_users_by_id(user_data):
    # Ordena usuarios por ID
    return sorted(user_data, key=lambda x: x['id'])