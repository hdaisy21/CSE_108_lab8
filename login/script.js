
// Function to handle user login
function login() {
    var username = document.getElementById("loginUsername").value;
    var password = document.getElementById("loginPassword").value;
    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/login";
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body = { "username": username, "password": password };
    xhttp.send(JSON.stringify(body));
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            const data = JSON.parse(this.responseText);
            var name = data.name; // Store the user's name in the global variable
            alert("Welcome " + name + "!");
            window.location.href = 'homepage.html';
            
        } else {
            alert("Error: " + xhttp.responseText); // Display error message from backend
        }
    };
}



// Function to handle user logout
function logout() {
    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/logout";
    xhttp.open("GET", url);
    xhttp.send();
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            window.location.replace('login.html'); // Redirect to login page
        } else {
            alert("Error: " + xhttp.responseText); // Display error message from backend
        }
    };
}

// Function to handle user registration
function submit() {
    var name = document.getElementById("name").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/user";
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body = {
        "name": name,
        "username": username,
        "password": password
    };
    xhttp.send(JSON.stringify(body));
    xhttp.onload = function () {
        if (xhttp.status >= 200 && xhttp.status < 300) {
            alert("User successfully registered"); // Alert success message
            window.location.replace('login.html');
        } else {
            alert("Error: " + xhttp.responseText); // Display error message from backend
        }
    };
}

// Function to access the protected route
function accessProtectedRoute() {
    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/protected";
    xhttp.open("GET", url);
    xhttp.send();
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            // Handle successful access to the protected route
            const data = JSON.parse(this.responseText);
            console.log(data.message);
            // Display protected content or perform further actions
        } else if (xhttp.status === 401) {
            // Handle unauthorized access
            alert("Unauthorized access: You need to log in to access this content.");
            // Redirect to the login page or display a message
            window.location.href = 'login.html';
        } else {
            // Handle other errors
            alert("Error accessing protected route: " + xhttp.responseText);
        }
    };
}


