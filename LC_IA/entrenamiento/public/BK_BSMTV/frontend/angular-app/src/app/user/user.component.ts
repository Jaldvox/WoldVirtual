export class UserComponent {
  users: any[] = [];
  
  constructor(private userService: UserService) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.userService.getUsers().subscribe((data: any[]) => {
      this.users = data;
    });
  }

  addUser(user: any) {
    this.userService.addUser(user).subscribe(() => {
      this.loadUsers();
    });
  }

  deleteUser(userId: number) {
    this.userService.deleteUser(userId).subscribe(() => {
      this.loadUsers();
    });
  }
}