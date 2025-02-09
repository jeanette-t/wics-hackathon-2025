const easyQuestions = [
    { question: "EASY: The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    },
    { question: "EASY: This apple tastes __ the red one.", choice1: "more sweet", choice2: "more sweet than", choice3: "sweeter", choice4: "sweeter than", correct: 4 },
    { question: "EASY: The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    }
];

const mediumQuestions = [
    { question: "MEDIUM: _______ washing his sweater, Jacob hung it up to dry", choice1: "After", choice2: "Before", choice3: "By", choice4: "Until", correct: 1 },
    { question: "MEDIUM: _______ you get a new haircut?", choice1: "Have", choice2: "Does", choice3: "Are", choice4: "Did", correct: 4 },
    { question: "MEDIUM: The first letter of the first word in a sentence should be", 
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
    { question: "HARD: The first letter of the first word in a sentence should be", 
        choice1: "a lowercase letter", 
        choice2: "an uppercase letter", 
        choice3: "a large letter", 
        choice4: "a small letter", 
        correct: 2 
    }
];

let prevDifficulty = "medium";
let currentDifficulty = "medium"; // Start at easy difficulty
let questionPool = [...mediumQuestions]; // Initial question pool
let usedQuestions = new Set(); // Track asked questions

const questionElement = document.querySelector("#question");
const scoreElement = document.querySelector("#score");
const choices = Array.from(document.querySelectorAll(".btn"));
const progressBar = document.querySelector("#progress-bar");

let currentQuestion = {};
let score = 0;
let correctStreak = 0;
let incorrectStreak = 0;
const MAX_QUESTIONS = 9;
let questionCount = 0;

function startQuiz() {
    score = 0;
    correctStreak = 0;
    incorrectStreak = 0;
    usedQuestions.clear(); // Reset used questions tracker
    updateQuestionPool();
    getNewQuestion();
}

function updateQuestionPool() {
    // Clear previous used questions when switching difficulty
    // usedQuestions.clear(); 

    if (currentDifficulty === "easy") {
        questionPool = [...easyQuestions];
    } else if (currentDifficulty === "medium") {
        questionPool = [...mediumQuestions];
    } else if (currentDifficulty === "hard") {
        questionPool = [...hardQuestions];
    }

    if (prevDifficulty !== currentDifficulty) {
        usedQuestions.clear(); 
    }
}

function getNewQuestion() {
    if (questionCount >= MAX_QUESTIONS) {
        localStorage.setItem("totalScore", score);
        document.getElementById("results-button").style.display = "block";
        return;
    }

    if (questionPool.length === 0 || usedQuestions.size >= MAX_QUESTIONS) {
        localStorage.setItem("totalScore", score);
        // Show the results button instead of redirecting
        document.getElementById("results-button").style.display = "block";
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
    
    questionElement.innerText = currentQuestion.question;

    choices.forEach((choice, index) => {
        choice.innerText = currentQuestion["choice" + (index + 1)];
    });

    progressBar.style.width = ((questionCount / MAX_QUESTIONS) * 100) + "%";
}

document.addEventListener("DOMContentLoaded", () => {
    const resultsButton = document.getElementById("results-button");
});

choices.forEach(choice => {
    choice.addEventListener("click", (e) => {
        questionCount++;
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset.number;

        const classToApply = parseInt(selectedAnswer) === currentQuestion.correct ? "correct" : "incorrect";

        if (selectedAnswer == currentQuestion.correct) {
            score++;
            correctStreak++;
            incorrectStreak = 0; // Reset incorrect streak
        } else {
            incorrectStreak++;
            correctStreak = 0; // Reset correct streak
        }
        scoreElement.innerText= score;

        if (correctStreak >= 2) {
            // Move from easy -> medium or medium -> hard
            if (currentDifficulty === "easy") {
                currentDifficulty = "medium";
            } else if (currentDifficulty === "medium") {
                currentDifficulty = "hard";
            }
        
            // Reset streaks after updating difficulty
            correctStreak = 0; // Reset correct streak after updating difficulty
            incorrectStreak = 0;
            
            // Update question pool with new difficulty
            updateQuestionPool(); 
        } 
        
        // Adjust difficulty after 2 incorrect answers in a row
        else if (incorrectStreak >= 2) {
            // Move from hard -> medium or medium -> easy
            if (currentDifficulty === "hard") {
                currentDifficulty = "medium";
            } else {
                currentDifficulty = "easy";
            }
        
            // Reset streaks after updating difficulty
            incorrectStreak = 0; // Reset incorrect streak after updating difficulty
            correctStreak = 0;
            
            // Update question pool with new difficulty
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