// Auto-redirect if already logged in
if (localStorage.getItem("loggedIn") === "true") {
    window.location.href = "index1.html"; // Correct redirect
}

// Toggle between forms
function toggleForm(form) {
    document.getElementById('loginForm').style.display = "none";
    document.getElementById('registerForm').style.display = "none";
    document.getElementById('forgotPasswordForm').style.display = "none";

    document.getElementById(form + 'Form').style.display = "flex";
}

// Show forgot password form
function showForgotPassword() {
    toggleForm('forgotPassword');
}

// Go back to login from forgot password
function backToLogin() {
    toggleForm('login');
}

// Handle login form submission
document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("loggedIn", "true");
            localStorage.setItem("username", username);
            alert(data.message || "Login successful!");
            window.location.href = "index1.html";
        } else {
            alert(data.detail || "Login failed. Check your credentials.");
        }
    } catch (error) {
        console.error("Error logging in:", error);
        alert("Something went wrong. Try again later.");
    }
});

// Handle register form submission
document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, username, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message || "Registration successful! Now you can log in.");
            toggleForm('login');
        } else {
            alert(data.detail || "Registration failed.");
        }
    } catch (error) {
        console.error("Error registering:", error);
        alert("Something went wrong. Try again later.");
    }
});

// Handle forgot password form submission
document.getElementById("forgotPasswordForm").addEventListener("submit", async function (e) {
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
            alert(data.message || "Password reset link sent! Check your email.");
            toggleForm('login');
        } else {
            alert(data.detail || "Failed to send reset link.");
        }
    } catch (error) {
        console.error("Error sending reset link:", error);
        alert("Something went wrong. Try again later.");
    }
});
