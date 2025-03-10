// Quiz questions database
const questions = [
    {
        category: "file",
        difficulty: "easy",
        question: "Which command would you use to list all files, including hidden ones?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _",
        options: ["ls -a", "ls -l", "ls -h", "ls -r"],
        correctIndex: 0,
        explanation: "The 'ls -a' command lists all files, including hidden files that start with a dot (.)"
    },
    {
        category: "navigation",
        difficulty: "easy",
        question: "Which command changes your current directory?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ /home/user/documents",
        options: ["cd", "pwd", "mv", "cp"],
        correctIndex: 0,
        explanation: "The 'cd' (change directory) command is used to navigate between folders."
    },
    {
        category: "process",
        difficulty: "medium",
        question: "Which command shows all running processes?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _",
        options: ["ps aux", "top", "proc", "tasks"],
        correctIndex: 0,
        explanation: "The 'ps aux' command shows all running processes with detailed information."
    },
    {
        category: "file",
        difficulty: "medium",
        question: "Which command is used to search for text within files?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ \"error\" /var/log/*.log",
        options: ["grep", "find", "search", "cat"],
        correctIndex: 0,
        explanation: "The 'grep' command searches for patterns in files using regular expressions."
    },
    {
        category: "system",
        difficulty: "hard",
        question: "Which command is used to manage system services in modern Linux distributions?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ start nginx",
        options: ["systemctl", "service", "init", "daemon"],
        correctIndex: 0,
        explanation: "The 'systemctl' command is used to control the systemd system and service manager."
    },
    {
        category: "network",
        difficulty: "medium",
        question: "Which command is used to transfer files from or to a server?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ file.txt user@server:/path/to/destination",
        options: ["scp", "ftp", "wget", "curl"],
        correctIndex: 0,
        explanation: "The 'scp' (secure copy) command uses SSH to transfer files between hosts."
    },
    {
        category: "file",
        difficulty: "easy",
        question: "Which command creates a new empty file?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ newfile.txt",
        options: ["touch", "create", "new", "mk"],
        correctIndex: 0,
        explanation: "The 'touch' command is used to create empty files or update timestamp on existing files."
    },
    {
        category: "system",
        difficulty: "medium",
        question: "Which command shows disk usage?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ -h",
        options: ["df", "du", "disk", "memory"],
        correctIndex: 0,
        explanation: "The 'df' (disk free) command shows available and used disk space on the system."
    },
    {
        category: "navigation",
        difficulty: "easy",
        question: "Which command shows your current directory?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _",
        options: ["pwd", "cd", "ls", "dir"],
        correctIndex: 0,
        explanation: "The 'pwd' (print working directory) command displays the current directory path."
    },
    {
        category: "process",
        difficulty: "hard",
        question: "Which command is used to kill a process by its ID?",
        terminal: "<span class=\"prompt\">user@shellwiz:~$</span> _ -9 1234",
        options: ["kill", "stop", "end", "terminate"],
        correctIndex: 0,
        explanation: "The 'kill' command is used to send signals to processes. The -9 option sends SIGKILL to forcefully terminate a process."
    }
];

// Game state variables
let currentQuestion = 0;
let score = 0;
let timer;
let timeRemaining = 30;
let answered = false;

// DOM elements
const questionElement = document.querySelector('.quiz-card h2');
const terminalOutput = document.querySelector('.terminal-output');
const optionsElements = document.querySelectorAll('.option');
const feedbackElement = document.querySelector('.feedback');
const progressBar = document.querySelector('.progress');
const nextButton = document.getElementById('next-btn');
const hintButton = document.getElementById('hint-btn');
const scoreDisplay = document.getElementById('current-score');
const questionDisplay = document.getElementById('current-question');
const timeDisplay = document.getElementById('time-remaining');
const gameOverScreen = document.querySelector('.game-over');
const finalScoreDisplay = document.querySelector('.final-score');
const playAgainButton = document.getElementById('play-again-btn');
const learnMoreButton = document.getElementById('learn-more-btn');
const quizCard = document.querySelector('.quiz-card');
const categoryBadge = document.querySelector('.category-badge');
const difficultyDots = document.querySelector('.difficulty');

// Initialize the game
function initGame() {
    loadQuestion(currentQuestion);
    addEventListeners();
}

// Load a question by index
function loadQuestion(index) {
    const question = questions[index];
    
    // Update question text
    questionElement.textContent = question.question;
    
    // Update terminal display
    terminalOutput.innerHTML = question.terminal;
    
    // Update options
    optionsElements.forEach((option, i) => {
        option.textContent = question.options[i];
        option.setAttribute('data-correct', i === question.correctIndex);
        option.classList.remove('correct', 'incorrect');
    });
    
    // Update category and difficulty
    categoryBadge.className = 'category-badge';
    categoryBadge.classList.add(`category-${question.category}`);
    categoryBadge.textContent = getCategoryName(question.category);
    
    difficultyDots.className = 'difficulty';
    difficultyDots.classList.add(`difficulty-${question.difficulty}`);
    
    // Update progress bar
    progressBar.style.width = `${((index + 1) / questions.length) * 100}%`;
    
    // Update question counter
    questionDisplay.textContent = index + 1;
    
    // Reset feedback
    feedbackElement.style.display = 'none';
    
    // Reset answered state
    answered = false;
    nextButton.disabled = true;
    
    // Start timer
    startTimer();
}

// Start the countdown timer
function startTimer() {
    clearInterval(timer);
    timeRemaining = 30;
    timeDisplay.textContent = timeRemaining;
    
    timer = setInterval(function() {
        timeRemaining--;
        timeDisplay.textContent = timeRemaining;
        
        if (timeRemaining <= 0) {
            clearInterval(timer);
            timeOut();
        }
    }, 1000);
}

// Handle time out
function timeOut() {
    if (!answered) {
        answered = true;
        
        // Highlight correct answer
        optionsElements.forEach((option, i) => {
            if (option.getAttribute('data-correct') === 'true') {
                option.classList.add('correct');
            }
        });
        
        showFeedback(false, "Time's up! " + questions[currentQuestion].explanation);
        nextButton.disabled = false;
    }
}

// Show feedback after answering
function showFeedback(correct, explanation) {
    feedbackElement.style.display = 'block';
    feedbackElement.classList.remove('correct', 'incorrect');
    feedbackElement.classList.add(correct ? 'correct' : 'incorrect');
    
    feedbackElement.querySelector('.feedback-content').textContent = correct ? 
        'Correct!' : 'Incorrect!';
    feedbackElement.querySelector('.feedback-explanation').textContent = explanation;
}

// Move to next question
function nextQuestion() {
    currentQuestion++;
    
    if (currentQuestion >= questions.length) {
        endGame();
    } else {
        loadQuestion(currentQuestion);
    }
}

// End the game and show results
function endGame() {
    quizCard.style.display = 'none';
    gameOverScreen.style.display = 'block';
    finalScoreDisplay.textContent = score;
    
    // In a real implementation, you would calculate achievements here
}

// Restart the game
function restartGame() {
    currentQuestion = 0;
    score = 0;
    scoreDisplay.textContent = score;
    
    quizCard.style.display = 'block';
    gameOverScreen.style.display = 'none';
    
    loadQuestion(0);
}

// Helper function to get category name
function getCategoryName(category) {
    const categories = {
        'file': 'File Operations',
        'navigation': 'Navigation',
        'process': 'Process Management',
        'network': 'Networking',
        'system': 'System Admin'
    };
    
    return categories[category] || category.charAt(0).toUpperCase() + category.slice(1);
}

// Add event listeners
function addEventListeners() {
    // Option click
    optionsElements.forEach(option => {
        option.addEventListener('click', function() {
            if (answered) return;
            answered = true;
            
            clearInterval(timer);
            const isCorrect = this.getAttribute('data-correct') === 'true';
            
            if (isCorrect) {
                this.classList.add('correct');
                showFeedback(true, questions[currentQuestion].explanation);
                score += 10;
                scoreDisplay.textContent = score;
            } else {
                this.classList.add('incorrect');
                
                // Find and highlight correct answer
                optionsElements.forEach(opt => {
                    if (opt.getAttribute('data-correct') === 'true') {
                        opt.classList.add('correct');
                    }
                });
                
                showFeedback(false, questions[currentQuestion].explanation);
            }
            
            nextButton.disabled = false;
        });
    });
    
    // Next button
    nextButton.addEventListener('click', nextQuestion);
    
    // Hint button
    hintButton.addEventListener('click', function() {
        score -= 5;
        scoreDisplay.textContent = score;
        
        // In a real implementation, provide helpful hints based on the current question
        const currentQuestionObj = questions[currentQuestion];
        const correctAnswer = currentQuestionObj.options[currentQuestionObj.correctIndex];
        
        alert(`Hint: This command starts with "${correctAnswer.charAt(0)}${correctAnswer.charAt(1)}"`);
    });
    
    // Play again button
    playAgainButton.addEventListener('click', restartGame);
    
    // Learn more button
    learnMoreButton.addEventListener('click', function() {
        alert('This would take you to the learning resources in a full implementation.');
    });
    
    // Quiz mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelector('.mode-btn.active').classList.remove('active');
            this.classList.add('active');
            alert('This would change the quiz mode in a full implementation.');
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initGame);