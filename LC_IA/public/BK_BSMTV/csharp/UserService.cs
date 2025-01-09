using System;
using System.Collections.Generic;

namespace MiProyectoAdministracion
{
    public class UserService
    {
        private List<User> users;

        public UserService()
        {
            users = new List<User>();
        }

        public void AddUser(User user)
        {
            users.Add(user);
        }

        public void RemoveUser(string userId)
        {
            users.RemoveAll(u => u.Id == userId);
        }

        public User GetUser(string userId)
        {
            return users.Find(u => u.Id == userId);
        }

        public List<User> GetAllUsers()
        {
            return users;
        }

        public void UpdateUser(User updatedUser)
        {
            var index = users.FindIndex(u => u.Id == updatedUser.Id);
            if (index != -1)
            {
                users[index] = updatedUser;
            }
        }
    }
}