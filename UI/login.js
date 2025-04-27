// Toggle between login and register forms
function toggleForm(form) {
    document.getElementById('loginForm').style.display = "none";
    document.getElementById('registerForm').style.display = "none";
    document.getElementById('forgotPasswordForm').style.display = "none";

    document.getElementById(form + 'Form').style.display = "flex";
}

// Show forgot password form
function showForgotPassword() {
    document.getElementById('loginForm').style.display = "none";
    document.getElementById('registerForm').style.display = "none";
    document.getElementById('forgotPasswordForm').style.display = "flex";
}

// Go back to login from forgot password
function backToLogin() {
    toggleForm('login');
}

// Handle login form submission
document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.querySelector('#loginForm input[type="text"]').value;
    const password = document.querySelector('#loginForm input[type="password"]').value;

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            sessionStorage.setItem("loggedIn", "true");
            alert("Login successful!");
            window.location.href = "index1.html";
        } else {
            alert(data.detail || "Login failed. Check your credentials.");
        }
    } catch (error) {
        console.error("Error logging in:", error);
        alert("Something went wrong. Try again.");
    }
});

// Handle register form submission
document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const full_name = document.querySelector('#registerForm input[placeholder="Full Name"]').value;
    const email = document.querySelector('#registerForm input[placeholder="Email"]').value;
    const username = document.querySelector('#registerForm input[placeholder="Username"]').value;
    const password = document.querySelector('#registerForm input[placeholder="Password"]').value;

    try {
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ full_name, email, username, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful! Now you can log in.");
            toggleForm('login');
        } else {
            alert(data.detail || "Registration failed.");
        }
    } catch (error) {
        console.error("Error registering:", error);
        alert("Something went wrong. Try again.");
    }
});

// Handle forgot password form submission
document.getElementById("forgotPasswordForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const email = document.getElementById("forgotEmail").value;

    try {
        const response = await fetch("http://localhost:8000/forgot-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Password reset link sent! Check your email.");
            toggleForm('login'); // Go back to login
        } else {
            alert(data.detail || "Failed to send reset link.");
        }
    } catch (error) {
        console.error("Error sending reset link:", error);
        alert("Something went wrong. Try again.");
    }
});
