// Smart College Assistant JavaScript

class SmartAssistant {
    constructor() {
        this.isDarkMode = localStorage.getItem('darkMode') === 'true';
        this.isListening = false;
        this.recognition = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeDarkMode();
        this.initializeVoiceRecognition();
        this.setupAutoComplete();
    }

    setupEventListeners() {
        // Send button
        document.getElementById('sendBtn').addEventListener('click', () => this.sendMessage());
        
        // Enter key
        document.getElementById('userInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Dark mode toggle
        document.getElementById('darkModeToggle').addEventListener('click', () => this.toggleDarkMode());

        // Voice toggle
        document.getElementById('voiceToggle').addEventListener('click', () => this.openVoiceModal());

        // Clear chat
        document.getElementById('clearChat').addEventListener('click', () => this.clearChat());

        // Voice controls
        document.getElementById('startVoice').addEventListener('click', () => this.startVoiceRecognition());
        document.getElementById('stopVoice').addEventListener('click', () => this.stopVoiceRecognition());

        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('voiceModal');
            if (e.target === modal) {
                this.closeVoiceModal();
            }
        });
    }

    initializeDarkMode() {
        if (this.isDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.getElementById('darkModeToggle').innerHTML = '<i class="fas fa-sun"></i>';
        }
    }

    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        localStorage.setItem('darkMode', this.isDarkMode);
        
        if (this.isDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.getElementById('darkModeToggle').innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.documentElement.removeAttribute('data-theme');
            document.getElementById('darkModeToggle').innerHTML = '<i class="fas fa-moon"></i>';
        }
    }

    initializeVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateVoiceStatus('Listening... Speak now!');
                this.updateVoiceIndicator(true);
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('userInput').value = transcript;
                this.closeVoiceModal();
                this.sendMessage();
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceStatus('Error: ' + event.error);
                this.isListening = false;
                this.updateVoiceIndicator(false);
            };

            this.recognition.onend = () => {
                this.isListening = false;
                this.updateVoiceIndicator(false);
            };
        } else {
            console.warn('Speech recognition not supported');
        }
    }

    setupAutoComplete() {
        const userInput = document.getElementById('userInput');
        const suggestionsContainer = document.getElementById('suggestions');
        let suggestionTimeout;
        
        // Create suggestions container if it doesn't exist
        if (!suggestionsContainer) {
            const container = document.createElement('div');
            container.id = 'suggestions';
            container.className = 'suggestions-container';
            userInput.parentNode.appendChild(container);
        }
        
        userInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            
            // Clear previous timeout
            clearTimeout(suggestionTimeout);
            
            if (query.length >= 2) {
                // Debounce the request
                suggestionTimeout = setTimeout(() => {
                    this.getSuggestions(query);
                }, 300);
            } else {
                this.hideSuggestions();
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.suggestions-container') && !e.target.closest('#userInput')) {
                this.hideSuggestions();
            }
        });
    }
    
    async getSuggestions(query) {
        try {
            const response = await fetch('/api/suggestions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            this.showSuggestions(data.suggestions);
        } catch (error) {
            console.error('Error getting suggestions:', error);
        }
    }
    
    showSuggestions(suggestions) {
        const container = document.getElementById('suggestions');
        if (!container) return;
        
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        container.innerHTML = suggestions.map(suggestion => `
            <div class="suggestion-item" data-type="${suggestion.type}" data-text="${suggestion.text}">
                <span class="suggestion-text">${suggestion.text}</span>
                <span class="suggestion-type">${suggestion.type}</span>
            </div>
        `).join('');
        
        // Add click handlers to suggestions
        container.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const text = e.currentTarget.dataset.text;
                document.getElementById('userInput').value = text;
                this.hideSuggestions();
                this.sendMessage();
            });
        });
        
        container.style.display = 'block';
    }
    
    hideSuggestions() {
        const container = document.getElementById('suggestions');
        if (container) {
            container.style.display = 'none';
        }
    }

    cycleHint() {
        const hints = [
            'Try: "Where is ME101?" or "Show ECE faculty"',
            'Ask: "Generate CSE timetable" or "Who teaches AI?"',
            'Say: "Find SF302" or "Show MECH faculty"'
        ];
        
        let currentHint = 0;
        const hintElement = document.getElementById('inputHints');
        
        setInterval(() => {
            if (!document.getElementById('userInput').value) {
                currentHint = (currentHint + 1) % hints.length;
                hintElement.textContent = hints[currentHint];
            }
        }, 3000);
    }

    async sendMessage() {
        const userInput = document.getElementById('userInput');
        const message = userInput.value.trim();
        
        if (message === '') return;
        
        // Add user message
        this.addMessage(message, true);
        
        // Clear input
        userInput.value = '';
        document.getElementById('inputHints').style.display = 'block';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(data.response, false, data.intent, data.confidence);
            
        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', false);
        }
    }

    addMessage(content, isUser = false, intent = null, confidence = null) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        
        // Format content with markdown-like formatting
        const formattedContent = this.formatMessage(content);
        messageText.innerHTML = formattedContent;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);
        
        // Add intent info for debugging (only in development)
        if (intent && confidence && window.location.hostname === 'localhost') {
            const intentInfo = document.createElement('div');
            intentInfo.className = 'intent-info';
            intentInfo.innerHTML = `<small>Intent: ${intent} (${(confidence * 100).toFixed(1)}%)</small>`;
            messageContent.appendChild(intentInfo);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    formatMessage(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/📍/g, '<span style="color: #48bb78;">📍</span>')
            .replace(/👨‍🏫/g, '<span style="color: #4299e1;">👨‍🏫</span>')
            .replace(/📅/g, '<span style="color: #ed8936;">📅</span>')
            .replace(/❌/g, '<span style="color: #f56565;">❌</span>')
            .replace(/✅/g, '<span style="color: #48bb78;">✅</span>');
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-text">
                    <div class="typing-indicator">
                        <span>Smart Assistant is thinking</span>
                        <div class="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }

    clearChat() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        <h4>👋 Welcome to Smart College Assistant!</h4>
                        <p>I'm powered by Machine Learning and can help you with:</p>
                        <ul>
                            <li>📍 <strong>Find Classrooms:</strong> "Where is EW212?"</li>
                            <li>👨‍🏫 <strong>Faculty Info:</strong> "Show CSE faculty"</li>
                            <li>📅 <strong>Timetables:</strong> "Generate MECH timetable"</li>
                            <li>🎤 <strong>Voice Input:</strong> Click the microphone button</li>
                        </ul>
                        <p>Try asking me anything!</p>
                    </div>
                    <div class="message-time">Just now</div>
                </div>
            </div>
        `;
    }

    openVoiceModal() {
        document.getElementById('voiceModal').style.display = 'block';
        this.updateVoiceStatus('Click to start speaking...');
    }

    closeVoiceModal() {
        document.getElementById('voiceModal').style.display = 'none';
        if (this.isListening) {
            this.stopVoiceRecognition();
        }
    }

    startVoiceRecognition() {
        if (this.recognition) {
            this.recognition.start();
            document.getElementById('startVoice').style.display = 'none';
            document.getElementById('stopVoice').style.display = 'inline-flex';
        } else {
            this.updateVoiceStatus('Voice recognition not supported in this browser');
        }
    }

    stopVoiceRecognition() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
        document.getElementById('startVoice').style.display = 'inline-flex';
        document.getElementById('stopVoice').style.display = 'none';
    }

    updateVoiceStatus(status) {
        document.getElementById('voiceStatus').textContent = status;
    }

    updateVoiceIndicator(isListening) {
        const indicator = document.getElementById('voiceIndicator');
        if (isListening) {
            indicator.style.background = 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)';
        } else {
            indicator.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }
}

// Global functions for quick actions
function askQuestion(question) {
    document.getElementById('userInput').value = question;
    smartAssistant.sendMessage();
}

function closeVoiceModal() {
    smartAssistant.closeVoiceModal();
}

// Initialize the Smart Assistant
let smartAssistant;
document.addEventListener('DOMContentLoaded', function() {
    smartAssistant = new SmartAssistant();
    
    // Focus on input
    document.getElementById('userInput').focus();
});

// Add some CSS for intent info
const style = document.createElement('style');
style.textContent = `
    .intent-info {
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: var(--text-muted);
        font-style: italic;
    }
`;
document.head.appendChild(style);
