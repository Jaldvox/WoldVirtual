#include "User.h"

User::User(int id, const std::string& name, const std::string& email) 
    : id(id), name(name), email(email) {}

int User::getId() const {
    return id;
}

std::string User::getName() const {
    return name;
}

std::string User::getEmail() const {
    return email;
}

void User::setName(const std::string& name) {
    this->name = name;
}

void User::setEmail(const std::string& email) {
    this->email = email;
}