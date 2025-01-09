export class UserService {
  private users: any[] = [];

  constructor() {}

  addUser(user: any): void {
    this.users.push(user);
  }

  getUsers(): any[] {
    return this.users;
  }

  updateUser(index: number, updatedUser: any): void {
    if (index >= 0 && index < this.users.length) {
      this.users[index] = updatedUser;
    }
  }

  deleteUser(index: number): void {
    if (index >= 0 && index < this.users.length) {
      this.users.splice(index, 1);
    }
  }
}