document.addEventListener('DOMContentLoaded', function() {
    const userForm = document.getElementById('userForm');
    const userList = document.getElementById('userList');

    userForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const userName = document.getElementById('userName').value;
        addUser(userName);
        userForm.reset();
    });

    function addUser(name) {
        const li = document.createElement('li');
        li.textContent = name;
        userList.appendChild(li);
    }
});