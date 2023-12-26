// users.js

document.addEventListener("DOMContentLoaded", function () {
    // Sample user data (replace with actual user data)
    const usersData = [
        { id: 1, username: 'user1', first_name: 'John', last_name: 'Doe' },
        { id: 2, username: 'user2', first_name: 'Jane', last_name: 'Smith' },
        // Add more user data as needed
    ];

    // Function to populate the list of users
    function populateUserList() {
        const userList = document.getElementById('userList');

        usersData.forEach(user => {
            const listItem = document.createElement('li');
            listItem.textContent = `${user.first_name} ${user.last_name}`;

            // Add a click event listener to show user details when clicked
            listItem.addEventListener('click', () => showUserDetails(user));

            userList.appendChild(listItem);
        });
    }

    // Function to display user details when a user is selected
    function showUserDetails(user) {
        const userDetails = document.getElementById('userDetails');

        // Create a card to display user details
        const card = document.createElement('div');
        card.classList.add('card');
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${user.first_name} ${user.last_name}</h5>
                <p class="card-text">Username: ${user.username}</p>
                <p class="card-text">ID: ${user.id}</p>
            </div>
        `;

        // Clear previous details and display the new user details
        userDetails.innerHTML = '';
        userDetails.appendChild(card);
    }

    // Initialize the user list
    populateUserList();
});
