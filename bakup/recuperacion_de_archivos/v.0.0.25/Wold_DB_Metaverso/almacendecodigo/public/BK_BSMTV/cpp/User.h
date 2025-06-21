// User.h
#ifndef USER_H
#define USER_H

#include <string>

class User {
public:
    User(int id, const std::string& name, const std::string& email);
    
    int getId() const;
    std::string getName() const;
    std::string getEmail() const;

    void setName(const std::string& name);
    void setEmail(const std::string& email);

private:
    int id;
    std::string name;
    std::string email;
};

#endif // USER_H