#include <iostream>
#include "User.h"

int main() {
    std::cout << "Bienvenido a la página de administración de usuarios." << std::endl;

    // Aquí puedes agregar la lógica para gestionar usuarios
    User user1("Juan", "juan@example.com");
    user1.displayInfo();

    // Más lógica de gestión de usuarios...

    return 0;
}