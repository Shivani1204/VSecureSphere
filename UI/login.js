const API_BASE = "http://3.110.193.27:31954";

// ===============================
// AUTO REDIRECT IF ALREADY LOGGED IN
// ===============================
if (localStorage.getItem("access_token") === "logged_in") {
    window.location.href = "homepage.html";
}

// ===============================
// FORM TOGGLE LOGIC
// ===============================
function toggleForm(form) {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("registerForm").style.display = "none";
    document.getElementById("forgotPasswordForm").style.display = "none";

    document.getElementById(form + "Form").style.display = "flex";
}

function showForgotPassword() {
    toggleForm("forgotPassword");
}

function backToLogin() {
    toggleForm("login");
}

// ===============================
// LOGIN
// ===============================
document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (!username || !password) {
        alert("Username and password are required");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        console.log("Login response:", data);

        if (!response.ok) {
            alert(data.detail || data.message || "Invalid login credentials");
            return;
        }

        // ✅ SAVE JWT + USER INFO
        localStorage.setItem("access_token", "logged_in");
        localStorage.setItem("username", username);

        alert("Login successful ✅");
        window.location.href = "homepage.html";

    } catch (error) {
        console.error("Login error:", error);
        alert("Server error. Please try again later.");
    }
});

// ===============================
// REGISTER
// ===============================
document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("registerName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const username = document.getElementById("registerUsername").value.trim();
    const password = document.getElementById("registerPassword").value.trim();

    if (!name || !email || !username || !password) {
        alert("All fields are required");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name,
                email,
                username,
                password
            })
        });

        const data = await response.json();
        console.log("Register response:", data);

        if (!response.ok) {
            alert(data.detail || data.message || "Registration failed");
            return;
        }

        alert("Registration successful 🎉 Please login.");
        toggleForm("login");

    } catch (error) {
        console.error("Register error:", error);
        alert("Server error. Please try again later.");
    }
});

// ===============================
// FORGOT PASSWORD
// ===============================
document.getElementById("forgotPasswordForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("forgotEmail").value.trim();

    if (!email) {
        alert("Email is required");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/forgot-password`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();
        console.log("Forgot password response:", data);

        if (!response.ok) {
            alert(data.detail || data.message || "Failed to send reset link");
            return;
        }

        alert("Password reset link sent 📩 Check your email.");
        toggleForm("login");

    } catch (error) {
        console.error("Forgot password error:", error);
        alert("Server error. Please try again later.");
    }
});
