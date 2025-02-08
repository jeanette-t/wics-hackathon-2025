// keep track of difficulty, if they get x amt wrong/correct move to more easy/difficult questions
const easyQuestions = [
    {
        question: "The first letter of the first word in a sentence should be",
        choice1: "a lowercase letter",
        choice2: "an uppercase letter",
        choice3: "a large letter",
        choice4: "a small letter",
        correct: 2
    },
    {
        question: "This apple tastes __ the red one.",
        choice1: "more sweet",
        choice2: "more sweet than",
        choice3: "sweeter",
        choice4: "sweeter than",
        correct: 4
    }
];

const mediumQuestions = [
    {
        question: "______ washing his sweater, Jacob hung it up to dry",
        choice1: "After",
        choice2: "Before",
        choice3: "By",
        choice4: "Until",
        correct: 1
    },
    {
        question: "_______ you get a new haircut?",
        choice1: "Have",
        choice2: "Does",
        choice3: "Are",
        choice4: "Did",
        correct: 4
    }
];

const hardQuestions = [
    {
        question: "Water __________ at a temperature of zero degrees Celsius.",
        choice1: "having frozen",
        choice2: "freezing",
        choice3: "freeze",
        choice4: "freezes",
        correct: 4
    },
    {
        question: "Identify the correctly punctuated sentence.",
        choice1: "I love to read; books are my escape.",
        choice2: "I love to read books, are my escape.",
        choice3: "I love to read: books, are my escape.",
        choice4: "I love to read; books, are my escape.",
        correct: 1
    }
];

let currentDifficulty = "medium"; // Start at medium difficulty
let questionPool = mediumQuestions; // Initial question pool

const question = document.querySelector("#question");
const choices = Array.from(document.querySelectorAll(".btn"));
const progressBar = document.querySelector("#progress-bar");

let currentQuestion = {};
let score = 0;
let currentQuestionIndex = 0;
let correctStreak = 0;
let incorrectStreak = 0;
const MAX_QUESTIONS = 5;

function startQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    correctStreak = 0;
    incorrectStreak = 0;
    updateQuestionPool();
    newQuestion();
}

function updateQuestionPool() {
    if (currentDifficulty === "easy") {
        questionPool = easyQuestions;
    } else if (currentDifficulty === "medium") {
        questionPool = mediumQuestions;
    } else if (currentDifficulty === "hard") {
        questionPool = hardQuestions;
    }
}

function newQuestion() {
    if (currentQuestionIndex >= MAX_QUESTIONS) {
        localStorage.setItem("totalScore", score);
        setTimeout(() => {
            return window.location.assign("/end.html");
        }, 1000);
    }

    let barWidth = (currentQuestionIndex / MAX_QUESTIONS) * 100;
    progressBar.style.width = barWidth + "%";

    // Get a random question from the pool
    currentQuestion = questionPool[Math.floor(Math.random() * questionPool.length)];
    question.innerText = (currentQuestionIndex + 1) + ". " + currentQuestion.question;

    choices.forEach((choice) => {
        const number = choice.dataset["number"];
        choice.innerText = currentQuestion["choice" + number];
    });

    currentQuestionIndex++;
}

choices.forEach((choice) => {
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
        if (correctStreak === 3 && currentDifficulty !== "hard") {
            currentDifficulty = currentDifficulty === "easy" ? "medium" : "hard";
            correctStreak = 0; // Reset streak
            updateQuestionPool();
        } else if (incorrectStreak === 3 && currentDifficulty !== "easy") {
            currentDifficulty = currentDifficulty === "hard" ? "medium" : "easy";
            incorrectStreak = 0; // Reset streak
            updateQuestionPool();
        }

        selectedChoice.classList.add(classToApply);

        setTimeout(() => {
            selectedChoice.classList.remove(classToApply);
            newQuestion();
        }, 1000);
    });
});

startQuiz();