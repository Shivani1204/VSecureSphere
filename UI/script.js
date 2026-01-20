// ===============================
// CONFIG
// ===============================
const API_BASE = "http://3.110.193.27:31201";

// Each HTML must define this:
// const EXPERIMENT_ID = "hping";

// ===============================
// ATTEMPTS COUNTER (per lab)
// ===============================
let attemptsKey = `${EXPERIMENT_ID}_attempts`;
let attempts = localStorage.getItem(attemptsKey)
    ? parseInt(localStorage.getItem(attemptsKey))
    : 0;

// ===============================
// MAIN FUNCTION
// ===============================
function checkAnswers() {
    let score = 0;
    let totalQuestions = 10;
    let unanswered = 0;

    attempts++;
    localStorage.setItem(attemptsKey, attempts);

    // Clear previous highlights
    document.querySelectorAll(".question").forEach((q) => {
        q.style.border = "";
        q.style.backgroundColor = "";
        q.querySelectorAll("label").forEach((label) => {
            label.style.color = "";
        });
    });

    for (let i = 1; i <= totalQuestions; i++) {
        const questionDiv = document.querySelector(`.question:nth-of-type(${i})`);
        const selectedOption = document.querySelector(`input[name="q${i}"]:checked`);
        const correctOption = document.querySelector(`input[name="q${i}"][value="correct"]`);

        if (!selectedOption) {
            unanswered++;
            questionDiv.style.border = "2px solid #2196F3";
            questionDiv.style.backgroundColor = "#E3F2FD";
        } else if (selectedOption.value === "correct") {
            score++;
            selectedOption.parentElement.style.color = "green";
            questionDiv.style.border = "2px solid green";
            questionDiv.style.backgroundColor = "#e6ffe6";
        } else {
            selectedOption.parentElement.style.color = "red";
            questionDiv.style.border = "2px solid red";
            questionDiv.style.backgroundColor = "#ffe6e6";
            correctOption.parentElement.style.color = "green";
        }
    }

    // ===============================
    // SHOW RESULT
    // ===============================
    const result = document.getElementById("result");
    result.innerHTML = `
        <h3>You scored ${score} out of ${totalQuestions}</h3>
        <p><strong>Attempt Number:</strong> ${attempts}</p>
    `;
    result.style.display = "flex";
    result.style.flexDirection = "column";
    result.style.alignItems = "center";

    const passed = score >= totalQuestions / 2;

    if (passed) {
        result.style.color = "green";
        result.innerHTML += `<p>✅ Passed</p>`;
    } else {
        result.style.color = "red";
        result.innerHTML += `<p>❌ Needs Improvement</p>`;
    }

    if (unanswered > 0) {
        result.innerHTML += `<p style="color: blue;">⚠️ ${unanswered} unanswered</p>`;
    }

    // ===============================
    // SAVE TO BACKEND
    // ===============================
    saveQuizResult(score, passed);
}

// ===============================
// BACKEND CALL
// ===============================
async function saveQuizResult(score, passed) {
    const username = localStorage.getItem("username");

    if (!username) {
        alert("Please login again");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/submit-knowledge-check`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                experiment_id: EXPERIMENT_ID,
                score: score,
                passed: passed
            })
        });

        const data = await response.json();
        console.log("Quiz saved:", data);

    } catch (error) {
        console.error("Error saving quiz:", error);
    }
}

// ===============================
// RESET (OPTIONAL)
// ===============================
function resetAttempts() {
    localStorage.removeItem(attemptsKey);
    attempts = 0;
}
