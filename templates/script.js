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
        var role = data.role;
        var name = data.name;
        alert("Logged in as: " + role + ", Welcome " + name + "!")
        if (role == 'admin')
            window.location.href = 'admin_dashboard.html'
        if (role == 'teacher')
            window.location.href = 'teacher_dashboard.html';
        if (role == 'user')
            window.location.href = 'student_dashboard.html';
        
            
        
        } else {
            alert("Error: " + xhttp.responseText); // Display error message from backend
        }
    };
}

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

function submit() {
    var name = document.getElementById("name").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var role = document.getElementById("role").value;

    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/user";
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body = {
        "name": name,
        "username": username,
        "password": password,
        "role": role
    };
    xhttp.send(JSON.stringify(body));
    xhttp.onload = function () {
        if (xhttp.status >= 200 && xhttp.status < 300) {
            alert("User successfully registered"); // Alert success message
        } else {
            alert("Error: " + xhttp.responseText); // Display error message from backend
        }
    };
}
