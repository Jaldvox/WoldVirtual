using System;

namespace MiProyectoAdministracion
{
    public class User
    {
        public int Id { get; set; }
        public string Nombre { get; set; }
        public string Email { get; set; }
        public string Contrasena { get; set; }

        public User(int id, string nombre, string email, string contrasena)
        {
            Id = id;
            Nombre = nombre;
            Email = email;
            Contrasena = contrasena;
        }

        public void MostrarInformacion()
        {
            Console.WriteLine($"ID: {Id}, Nombre: {Nombre}, Email: {Email}");
        }
    }
}