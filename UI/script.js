function checkAnswers() {
    let score = 0;
    let totalQuestions = 10; // Update this to the total number of questions
    let unanswered = 0;

    // Loop through all questions dynamically
    for (let i = 1; i <= totalQuestions; i++) {
        const selectedOption = document.querySelector(`input[name="q${i}"]:checked`);
        
        if (!selectedOption) {
            unanswered++; // Count unanswered questions
        } else if (selectedOption.value === "correct") {
            score++;
        }
    }

    // Display result message
    const result = document.getElementById('result');
    result.innerHTML = `<h3>You scored ${score} out of ${totalQuestions}</h3>`;

    // Centering styles for result
    result.style.textAlign = "center"; // Center text
    result.style.marginTop = "20px";
    result.style.padding = "15px";
    result.style.fontSize = "18px";
    result.style.fontWeight = "bold";
    result.style.display = "flex";  
    result.style.flexDirection = "column";  
    result.style.alignItems = "center";  
    result.style.justifyContent = "center";

    // Change result color and add feedback message
    if (score === totalQuestions) {
        result.style.color = "green";
        result.innerHTML += `<p style="color: green; font-size: 18px;">🎉 Excellent! Perfect Score! 🎉</p>`;
    } else if (score >= totalQuestions / 2) {
        result.style.color = "orange";
        result.innerHTML += `<p style="color: orange; font-size: 18px;">😊 Good job! Keep improving! 😊</p>`;
    } else {
        result.style.color = "red";
        result.innerHTML += `<p style="color: red; font-size: 18px; text-align: center;">💡 Needs Improvement. Try again! 💡</p>`;
    }

    // Warn about unanswered questions
    if (unanswered > 0) {
        result.innerHTML += `<p style="color: blue; font-size: 16px;">⚠️ You left ${unanswered} question(s) unanswered.</p>`;
    }
}
