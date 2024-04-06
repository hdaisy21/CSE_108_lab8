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
            // Login successful, redirect to homepage
            
            window.location.href = 'homepage.html';
        } else {
            // Login failed, display error message from the backend
            alert("Error: " + xhttp.responseText);
        }
    };
}

function submit(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/user";
    //const url = "https://amhep.pythonanywhere.com/grades";
    const async = true;
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body ={"username": username, "password": password};
    xhttp.send(JSON.stringify(body));
    xhttp.onload = function() {
    if (xhttp.status >= 200 && xhttp.status < 300) {
        alert(xhttp.responseText);
    } else {
        alert("Error: " + xhttp.responseText);
    } 
    };

}

// function fetchUsername() {
//     var xhttp = new XMLHttpRequest();
//     xhttp.open("GET", "/username");
//     xhttp.send();
//     xhttp.onload = function () {
//         if (xhttp.status === 200) {
//             var username = JSON.parse(xhttp.responseText).username;
//             document.getElementById("username-placeholder").innerText = username;
//         } else {
//             console.error("Error fetching username: " + xhttp.responseText);
//         }
//     };
// }

// // Call fetchUsername() when the page loads
// window.onload = function () {
//     fetchUsername();
// };

function logout() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/logout");
    xhttp.send();
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            // Clear any local user-related data (if any)
            // Redirect to login page or perform any other action
            window.location.href = 'login.html'; // Example: Redirect to login page
        } else {
            alert("Error: " + xhttp.responseText);
        }
    };
}