const API_BASE = "http://3.110.193.27:31201";

async function finishLab() {
    const username = localStorage.getItem("username");

    if (!username) {
        alert("Please login again");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/complete-lab`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                experiment_id: EXPERIMENT_ID
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to mark lab complete");
            return;
        }

        alert("Lab completed successfully ✅");
        window.location.href = "homepage.html";

    } catch (err) {
        console.error(err);
        alert("Server not reachable");
    }
}