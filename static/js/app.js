// Chat functionality
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const statusElement = document.getElementById('status');

// Add message to chat
function addMessage(content, type = 'bot', toolInfo = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    let messageHTML = `<div class="message-content">`;
    
    if (type === 'user') {
        messageHTML += `<strong>You:</strong> ${escapeHtml(content)}`;
    } else if (type === 'bot') {
        messageHTML += `<strong>AI Assistant:</strong> ${escapeHtml(content)}`;
    } else if (type === 'loading') {
        messageHTML += `<strong>Processing...</strong> ${escapeHtml(content)}`;
    } else if (type === 'error') {
        messageHTML += `<strong>Error:</strong> ${escapeHtml(content)}`;
    }
    
    messageHTML += `</div>`;
    
    // Add tool information if available
    if (toolInfo) {
        messageHTML += `<div class="tool-info">🔧 Used tool: ${escapeHtml(toolInfo)}</div>`;
    }
    
    messageDiv.innerHTML = messageHTML;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Update status
function updateStatus(text, color = '#28a745') {
    statusElement.innerHTML = `<span class="status-dot" style="background: ${color}"></span> ${text}`;
}

// Send query to backend
async function sendQuery() {
    const query = userInput.value.trim();
    
    if (!query) {
        return;
    }
    
    // Disable input
    sendButton.disabled = true;
    userInput.disabled = true;
    
    // Add user message
    addMessage(query, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Add loading message
    const loadingMsg = addMessage('Analyzing your query and fetching data...', 'loading');
    updateStatus('Processing...', '#ffc107');
    
    try {
        // Send request to backend
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        // Remove loading message
        loadingMsg.remove();
        
        if (data.success) {
            // Add bot response
            addMessage(
                data.response, 
                'bot',
                data.tool_used ? data.tool_used : null
            );
            updateStatus('Ready', '#28a745');
        } else {
            // Add error message
            addMessage(
                data.response || 'An error occurred while processing your request.',
                'error'
            );
            updateStatus('Error occurred', '#dc3545');
        }
        
    } catch (error) {
        console.error('Error:', error);
        loadingMsg.remove();
        addMessage(
            'Failed to connect to the server. Please try again.',
            'error'
        );
        updateStatus('Connection error', '#dc3545');
    }
    
    // Re-enable input
    sendButton.disabled = false;
    userInput.disabled = false;
    userInput.focus();
}

// Set query from example
function setQuery(text) {
    userInput.value = text;
    userInput.focus();
}

// Enter key to send
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuery();
    }
});

// Check health on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateStatus('Connected & Ready', '#28a745');
        } else {
            updateStatus('Service issues detected', '#ffc107');
        }
    } catch (error) {
        updateStatus('Unable to connect', '#dc3545');
    }
});