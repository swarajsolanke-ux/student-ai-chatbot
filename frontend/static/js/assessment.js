// assessment.js - AI Assessment Chatbot Functionality
const assessmentQuestions = [
    {
        step: 1,
        category: "Personality",
        question: "Let's start with your personality! How would you describe yourself in social situations?",
        quickAnswers: ["I'm outgoing and energetic", "I prefer smaller groups", "I'm introverted and reflective", "It depends on the situation"]
    },
    {
        step: 2,
        category: "Academic Strengths",
        question: "What subjects or areas do you excel in academically?",
        quickAnswers: ["Math & Sciences", "Languages & Arts", "Technology & Engineering", "Business & Economics"]
    },
    {
        step: 3,
        category: "Thinking Style",
        question: "How do you approach problem-solving?",
        quickAnswers: ["Logical and analytical", "Creative and innovative", "Practical and hands-on", "Collaborative and team-oriented"]
    },
    {
        step: 4,
        category: "Learning Style",
        question: "How do you learn best?",
        quickAnswers: ["Visual (diagrams, videos)", "Auditory (lectures, discussions)", "Practical (doing, experiments)", "Reading and writing"]
    },
    {
        step: 5,
        category: "Interests",
        question: "What topics or activities interest you most?",
        quickAnswers: ["Technology & Innovation", "Healthcare & Medicine", "Arts & Design", "Business & Finance", "Science & Research"]
    },
    {
        step: 6,
        category: "Career Tendencies",
        question: "What kind of career environment appeals to you?",
        quickAnswers: ["Corporate/Office", "Research/Academic", "Creative Studio", "Startup/Entrepreneurship", "Social Impact/NGO"]
    }
];

let currentQuestion = 0;
let assessmentData = {
    answers: []
};

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return;
    }

    // Setup event listeners
    setupEventListeners();

    // Start assessment after a brief delay
    setTimeout(() => {
        askQuestion(0);
    }, 1500);
});

function setupEventListeners() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });

    // Send on Enter (Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendAnswer();
        }
    });

    sendBtn.addEventListener('click', sendAnswer);
}

function askQuestion(index) {
    if (index >= assessmentQuestions.length) {
        processAssessment();
        return;
    }

    const question = assessmentQuestions[index];
    currentQuestion = index;

    // Update progress
    const progress = ((index + 1) / assessmentQuestions.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('currentStep').textContent = `Step ${index + 1}`;
    document.getElementById('totalSteps').textContent = assessmentQuestions.length;

    // Show typing indicator
    showTypingIndicator();

    setTimeout(() => {
        hideTypingIndicator();
        addAIMessage(question.question);
        showQuickAnswers(question.quickAnswers);
        enableInput();
    }, 1000);
}

function addAIMessage(message) {
    const chatContainer = document.getElementById('chatContainer');
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';

    messageGroup.innerHTML = `
        <div class="ai-avatar">🤖</div>
        <div class="message-bubble ai-message">
            <p>${message}</p>
        </div>
    `;

    chatContainer.appendChild(messageGroup);
    scrollToBottom();
}

function addUserMessage(message) {
    const chatContainer = document.getElementById('chatContainer');
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group user';

    const userInitial = localStorage.getItem('userInitial') || 'U';

    messageGroup.innerHTML = `
        <div class="user-avatar">${userInitial}</div>
        <div class="message-bubble user-message">
            <p>${message}</p>
        </div>
    `;

    chatContainer.appendChild(messageGroup);
    scrollToBottom();
}

function showTypingIndicator() {
    const chatContainer = document.getElementById('chatContainer');
    const indicator = document.createElement('div');
    indicator.className = 'message-group typing';
    indicator.id = 'typingIndicator';

    indicator.innerHTML = `
        <div class="ai-avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;

    chatContainer.appendChild(indicator);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function showQuickAnswers(answers) {
    const quickActions = document.getElementById('quickActions');
    quickActions.innerHTML = '';

    answers.forEach(answer => {
        const btn = document.createElement('button');
        btn.className = 'quick-btn';
        btn.textContent = answer;
        btn.onclick = () => selectQuickAnswer(answer);
        quickActions.appendChild(btn);
    });
}

function selectQuickAnswer(answer) {
    document.getElementById('userInput').value = answer;
    sendAnswer();
}

function enableInput() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
}

function disableInput() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    userInput.disabled = true;
    sendBtn.disabled = true;
}

function sendAnswer() {
    const userInput = document.getElementById('userInput');
    const answer = userInput.value.trim();

    if (!answer) return;

    // Add user message
    addUserMessage(answer);

    // Store answer
    const question = assessmentQuestions[currentQuestion];
    assessmentData.answers.push({
        category: question.category,
        question: question.question,
        answer: answer
    });

    // Clear input and quick answers
    userInput.value = '';
    userInput.style.height = 'auto';
    document.getElementById('quickActions').innerHTML = '';
    disableInput();

    // Move to next question
    setTimeout(() => {
        askQuestion(currentQuestion + 1);
    }, 500);
}

async function processAssessment() {
    disableInput();
    document.getElementById('quickActions').innerHTML = '';

    showTypingIndicator();

    addAIMessage("Thank you for completing the assessment! Let me analyze your responses and find the perfect majors for you...");

    try {
        const response = await authenticatedFetch('/assessment/evaluate', {
            method: 'POST',
            body: JSON.stringify({
                test_type: 'comprehensive',
                answers: assessmentData.answers
            })
        });

        if (response.ok) {
            const results = await response.json();
            console.log("results",results)
            hideTypingIndicator();

            setTimeout(() => {
                showResults(results);
            }, 1500);
        } else {
            hideTypingIndicator();
            addAIMessage("I apologize, but I encountered an error processing your assessment. Please try again.");
            enableInput();
        }
    } catch (error) {
        console.error('Assessment error:', error);
        hideTypingIndicator();
        addAIMessage("I apologize, but I encountered an error. Please try again or contact support.");
    }
}

function showResults(results) {
    const modal = document.getElementById('resultsModal');
    const content = document.getElementById('resultsContent');

    const recommendations = results.recommendations || [];

    let html = '';

    if (recommendations.length === 0) {
        html = '<p>No recommendations available. Please complete your profile for better results.</p>';
    } else {
        recommendations.forEach((major, index) => {
            const matchPercent = Math.round(major.match_score * 100);

            html += `
                <div class="major-card">
                    <div class="major-header">
                        <h3 class="major-title">${index + 1}. ${major.major_name}</h3>
                        <span class="match-score">${matchPercent}% Match</span>
                    </div>
                    
                    <p><strong>Why this major?</strong> ${major.explanation}</p>
                    
                    <div class="major-meta">
                        <div class="meta-item">
                            <div class="meta-label">Difficulty</div>
                            <div class="meta-value">${major.difficulty_level}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Estimated Cost</div>
                            <div class="meta-value">$${major.estimated_cost?.toLocaleString() || 'N/A'}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Duration</div>
                            <div class="meta-value">${major.study_duration || '3-4 years'}</div>
                        </div>
                    </div>f
                    
                    <p><strong>Career Opportunities:</strong> ${major.career_paths}</p>
                    
                    <div class="roadmap">
                        <h4>📚 Your Study Roadmap:</h4>
                        <ol>
                            ${major.roadmap?.map(step => `<li>${step}</li>`).join('') || '<li>No roadmap available</li>'}
                        </ol>
                    </div>
                </div>
            `;
        });
    }

    content.innerHTML = html;
    modal.classList.add('show');
}

function closeResults() {
    document.getElementById('resultsModal').classList.remove('show');
}

function viewUniversities() {
    window.location.href = '/universities';
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
