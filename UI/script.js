// Initialize attempts counter
let attempts = localStorage.getItem('hping_attempts') ? parseInt(localStorage.getItem('hping_attempts')) : 0;

function checkAnswers() {
    let score = 0;
    let totalQuestions = 10;
    let unanswered = 0;

    // Increase attempt count
    attempts++;
    localStorage.setItem('hping_attempts', attempts);

    // Clear previous highlights
    document.querySelectorAll(".question").forEach((q) => {
        q.style.border = "";
        q.style.backgroundColor = "";
        q.querySelectorAll('label').forEach((label) => {
            label.style.color = ""; // reset label colors
        });
    });

    for (let i = 1; i <= totalQuestions; i++) {
        const questionDiv = document.querySelector(`.question:nth-of-type(${i})`);
        const selectedOption = document.querySelector(`input[name="q${i}"]:checked`);
        const correctOption = document.querySelector(`input[name="q${i}"][value="correct"]`);

        if (!selectedOption) {
            unanswered++;
            questionDiv.style.border = "2px solid #2196F3";
            questionDiv.style.backgroundColor = "#E3F2FD"; // Light blue for unanswered
        } else if (selectedOption.value === "correct") {
            score++;
            selectedOption.parentElement.style.color = "green";
            questionDiv.style.border = "2px solid green";
            questionDiv.style.backgroundColor = "#e6ffe6"; // light green background
        } else {
            selectedOption.parentElement.style.color = "red";
            questionDiv.style.border = "2px solid red";
            questionDiv.style.backgroundColor = "#ffe6e6"; // light red background
            correctOption.parentElement.style.color = "green"; // highlight correct answer
        }
    }

    // Display result
    const result = document.getElementById('result');
    result.innerHTML = `<h3>You scored ${score} out of ${totalQuestions}</h3>
                        <p><strong>Attempt Number:</strong> ${attempts}</p>`;
    result.style.textAlign = "center";
    result.style.marginTop = "20px";
    result.style.padding = "15px";
    result.style.fontSize = "18px";
    result.style.fontWeight = "bold";
    result.style.display = "flex";  
    result.style.flexDirection = "column";  
    result.style.alignItems = "center";  
    result.style.justifyContent = "center";

    if (score === totalQuestions) {
        result.style.color = "green";
        result.innerHTML += `<p style="color: green;">🎉 Excellent! Perfect Score! 🎉</p>`;
    } else if (score >= totalQuestions / 2) {
        result.style.color = "orange";
        result.innerHTML += `<p style="color: orange;">😊 Good job! Keep improving! 😊</p>`;
    } else {
        result.style.color = "red";
        result.innerHTML += `<p style="color: red;">💡 Needs Improvement. Try again! 💡</p>`;
    }

    if (unanswered > 0) {
        result.innerHTML += `<p style="color: blue;">⚠️ You left ${unanswered} question(s) unanswered.</p>`;
    }

    saveQuizResult(score, EXPERIMENT_ID);

    async function saveQuizResult(score, experimentId) {
        const username = localStorage.getItem("username");
        const API_BASE = "http://3.110.193.27:31201";

        if (!username) {
            console.warn("User not logged in");
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/submit-knowledge-check`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: username,
                    experiment_id: experimentId,
                    score: score,
                    passed: score >= 5   // pass criteria
                })
            });

            const data = await response.json();
            console.log("Quiz saved to backend:", data);

        } catch (err) {
            console.error("Error saving quiz:", err);
        }
    }

}

// Optional: Reset attempts (for testing or if you want a reset button)
function resetAttempts() {
    localStorage.removeItem('hping_attempts');
    attempts = 0;
}
