// Point to your live backend (use an empty string "" if using the monolithic setup)
const API_BASE_URL = "https://fiscaldashboard.onrender.com"; 

const chatOutput = document.getElementById('chat-output');
const chatInput = document.getElementById('chat-input');
const chatSubmit = document.getElementById('chat-submit');

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    
    // Style differently based on who is speaking (User vs AI)
    if (sender === 'user') {
        msgDiv.className = 'bg-primary/20 text-on-surface p-3 rounded-lg rounded-tr-none self-end w-10/12 border border-primary/30 shadow-sm ml-auto mt-4';
    } else {
        msgDiv.className = 'bg-surface-container-high text-on-surface p-3 rounded-lg rounded-tl-none self-start w-10/12 border border-white/5 shadow-sm mt-4';
    }
    
    msgDiv.textContent = text;
    chatOutput.appendChild(msgDiv);
    
    // Auto-scroll to the bottom
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

async function handleChatSubmit() {
    const prompt = chatInput.value.trim();
    if (!prompt) return;

    // 1. Display user message and clear input
    appendMessage('user', prompt);
    chatInput.value = '';

    // 2. Display a temporary "Thinking..." state
    const loadingId = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.id = loadingId;
    loadingDiv.className = 'bg-surface-container-high text-on-surface-variant p-3 rounded-lg rounded-tl-none self-start w-10/12 border border-white/5 shadow-sm mt-4 italic';
    loadingDiv.innerHTML = '<span class="animate-pulse">Analyzing data...</span>';
    chatOutput.appendChild(loadingDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    try {
        // 3. Send the prompt to your backend FastAPI route
        const response = await fetch(`${API_BASE_URL}/api/v1/chat/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });

        const result = await response.json();
        
        // 4. Remove the loading indicator and display the real answer
        document.getElementById(loadingId).remove();
        appendMessage('ai', result.response);

    } catch (error) {
        console.error("Chat API Error:", error);
        document.getElementById(loadingId).remove();
        appendMessage('ai', 'Connection error. The AI Agent is currently unreachable.');
    }
}

// Event Listeners for clicking the button or pressing "Enter"
chatSubmit.addEventListener('click', handleChatSubmit);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChatSubmit();
});
