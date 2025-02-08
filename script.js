const easyQuestions = [
    { question: "EASY: The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    },
    { question: "EASY: This apple tastes __ the red one.", choice1: "more sweet", choice2: "more sweet than", choice3: "sweeter", choice4: "sweeter than", correct: 4 },
    { question: "EASY 3 The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    }
];

const mediumQuestions = [
    { question: "MEDIUM: ______ washing his sweater, Jacob hung it up to dry", choice1: "After", choice2: "Before", choice3: "By", choice4: "Until", correct: 1 },
    { question: "MEDIUM: _______ you get a new haircut?", choice1: "Have", choice2: "Does", choice3: "Are", choice4: "Did", correct: 4 },
    { question: "MEDIUM 3 The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    }
];

const hardQuestions = [
    { question: "HARD: Water __________ at a temperature of zero degrees Celsius.", choice1: "having frozen", choice2: "freezing", choice3: "freeze", choice4: "freezes", correct: 4 },
    { question: "HARD: Identify the correctly punctuated sentence.", choice1: "I love to read; books are my escape.", choice2: "I love to read books, are my escape.", choice3: "I love to read: books, are my escape.", choice4: "I love to read; books, are my escape.", correct: 1 },
    { question: "HARD 3 The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    }
];

let currentDifficulty = "medium"; // Start at medium difficulty
let questionPool = [...mediumQuestions]; // Initial question pool
let usedQuestions = new Set(); // Track asked questions

const questionElement = document.querySelector("#question");
const choices = Array.from(document.querySelectorAll(".btn"));
const progressBar = document.querySelector("#progress-bar");

let currentQuestion = {};
let score = 0;
let correctStreak = 0;
let incorrectStreak = 0;
const MAX_QUESTIONS = 5;

function startQuiz() {
    score = 0;
    correctStreak = 0;
    incorrectStreak = 0;
    usedQuestions.clear(); // Reset used questions tracker
    updateQuestionPool();
    newQuestion();
}

function updateQuestionPool() {
    if (currentDifficulty === "easy") {
        questionPool = [...easyQuestions];
    } else if (currentDifficulty === "medium") {
        questionPool = [...mediumQuestions];
    } else if (currentDifficulty === "hard") {
        questionPool = [...hardQuestions];
    }
}

function getNewQuestion() {
    if (questionPool.length === 0 || usedQuestions.size >= MAX_QUESTIONS) {
        localStorage.setItem("totalScore", score);
        setTimeout(() => window.location.href = "results.html", 1000);
        return;
    }

    // Select a new question that hasn't been used
    let availableQuestions = questionPool.filter(q => !usedQuestions.has(q.question));
    
    if (availableQuestions.length === 0) {
        updateQuestionPool(); // Reset pool when all questions are used
        availableQuestions = questionPool.filter(q => !usedQuestions.has(q.question));
    }

    currentQuestion = availableQuestions[Math.floor(Math.random() * availableQuestions.length)];
    usedQuestions.add(currentQuestion.question); // Mark as used

    questionElement.innerText = (usedQuestions.size) + ". " + currentQuestion.question;

    choices.forEach((choice, index) => {
        choice.innerText = currentQuestion["choice" + (index + 1)];
    });

    progressBar.style.width = ((usedQuestions.size / MAX_QUESTIONS) * 100) + "%";
}

choices.forEach(choice => {
    choice.addEventListener("click", (e) => {
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset["number"];

        const classToApply = selectedAnswer == currentQuestion.correct ? "correct" : "incorrect";

        if (selectedAnswer == currentQuestion.correct) {
            score++;
            correctStreak++;
            incorrectStreak = 0; // Reset incorrect streak
        } else {
            incorrectStreak++;
            correctStreak = 0; // Reset correct streak
        }

        // Adjust difficulty after 3 correct/incorrect answers in a row
        if (correctStreak === 2 && currentDifficulty !== "hard") {
            currentDifficulty = currentDifficulty === "easy" ? "medium" : "hard";
            correctStreak = 0;
            updateQuestionPool();
        } else if (incorrectStreak === 2 && currentDifficulty !== "easy") {
            currentDifficulty = currentDifficulty === "hard" ? "medium" : "easy";
            incorrectStreak = 0;
            updateQuestionPool();
        }

        selectedChoice.classList.add(classToApply);

        setTimeout(() => {
            selectedChoice.classList.remove(classToApply);
            getNewQuestion();
        }, 1000);
    });
});

startQuiz();