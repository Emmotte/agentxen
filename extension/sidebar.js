/**
 * AgentXen Sidebar Chat Interface
 */

const messagesDiv = document.getElementById('messages');
const commandInput = document.getElementById('command-input');
const sendBtn = document.getElementById('send-btn');
const statusIndicator = document.getElementById('status');

let agentConnected = false;

// Add message to chat
function addMessage(text, type = 'agent') {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = text;
  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Send command to agent
async function sendCommand() {
  const command = commandInput.value.trim();
  if (!command) return;
  
  // Add user message
  addMessage(command, 'user');
  commandInput.value = '';
  
  // Disable input while processing
  sendBtn.disabled = true;
  commandInput.disabled = true;
  
  try {
    // Send to background script
    const response = await browser.runtime.sendMessage({
      type: 'send-command',
      command: { text: command }
    });
    
    if (!response.success) {
      throw new Error(response.error || 'Failed to send command');
    }
    
    addMessage('Processing...', 'system');
    
  } catch (error) {
    console.error('Error sending command:', error);
    addMessage(`❌ Error: ${error.message}`, 'system');
  } finally {
    sendBtn.disabled = false;
    commandInput.disabled = false;
    commandInput.focus();
  }
}

// Listen for agent responses
browser.runtime.onMessage.addListener((message) => {
  if (message.type === 'agent-response') {
    const data = message.data;
    
    if (data.type === 'status') {
      addMessage(data.message, 'agent');
    } else if (data.type === 'result') {
      const resultText = data.success 
        ? `✅ ${data.message || 'Done!'}`
        : `❌ ${data.message || 'Failed'}`;
      addMessage(resultText, 'agent');
    }
  } else if (message.type === 'agent-connected') {
    agentConnected = true;
    statusIndicator.classList.add('connected');
    addMessage('✅ Connected to AgentXen agent', 'system');
  } else if (message.type === 'agent-disconnected') {
    agentConnected = false;
    statusIndicator.classList.remove('connected');
    addMessage('⚠️ Disconnected from agent. Reconnecting...', 'system');
  }
});

// Check agent status on load
browser.runtime.sendMessage({ type: 'check-agent-status' })
  .then(response => {
    agentConnected = response.connected;
    if (agentConnected) {
      statusIndicator.classList.add('connected');
    }
  });

// Event listeners
sendBtn.addEventListener('click', sendCommand);
commandInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendCommand();
  }
});

// Example commands
document.querySelectorAll('.example-cmd').forEach(cmd => {
  cmd.addEventListener('click', () => {
    commandInput.value = cmd.textContent;
    commandInput.focus();
  });
});

console.log('🚀 AgentXen sidebar loaded');
