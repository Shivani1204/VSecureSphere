// Toggle between login and register forms
function toggleForm(form) {
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('registerForm').classList.remove('active');
    document.getElementById(form + 'Form').classList.add('active');
}

// Handle login form submission
document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault();  // Prevent the default form submission

    // Get the username and password input values
    const username = document.querySelector('#loginForm input[type="text"]').value;
    const password = document.querySelector('#loginForm input[type="password"]').value;

    // Debugging: Log the entered username and password
    console.log("Username:", username);
    console.log("Password:", password);

    // Simple validation (replace with actual authentication logic if necessary)
    if (username === "admin" && password === "1234") {
        // Optionally store the login state in sessionStorage
        sessionStorage.setItem("loggedIn", "true");

        // Redirect to index1.html after successful login
        window.location.href = "index1.html";
    } else {
        alert("Invalid username or password.");
    }
});
