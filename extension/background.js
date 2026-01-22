/**
 * AgentXen Background Script
 * Handles communication between browser extension and native Python agent
 */

let nativePort = null;
let agentConnected = false;

// Connect to native messaging host (Python agent)
function connectToAgent() {
  console.log('🔌 Connecting to AgentXen native host...');
  
  try {
    nativePort = browser.runtime.connectNative('agentxen');
    
    nativePort.onMessage.addListener((message) => {
      console.log('📨 Message from agent:', message);
      
      // Broadcast to sidebar and popup
      browser.runtime.sendMessage({
        type: 'agent-response',
        data: message
      }).catch(err => {
        // Ignore if no listeners
      });
      
      // Handle different message types
      if (message.type === 'action-result') {
        handleActionResult(message.data);
      }
    });
    
    nativePort.onDisconnect.addListener(() => {
      console.log('⚠️ Disconnected from agent');
      agentConnected = false;
      
      // Notify UI
      browser.runtime.sendMessage({
        type: 'agent-disconnected'
      }).catch(err => {});
      
      // Attempt reconnect after 5 seconds
      setTimeout(connectToAgent, 5000);
    });
    
    agentConnected = true;
    console.log('✅ Connected to AgentXen agent');
    
    // Notify UI
    browser.runtime.sendMessage({
      type: 'agent-connected'
    }).catch(err => {});
    
  } catch (error) {
    console.error('❌ Failed to connect to agent:', error);
    agentConnected = false;
    
    // Retry connection
    setTimeout(connectToAgent, 5000);
  }
}

// Send command to agent
function sendToAgent(command) {
  if (!agentConnected || !nativePort) {
    console.error('❌ Agent not connected');
    return Promise.reject(new Error('Agent not connected'));
  }
  
  console.log('📤 Sending to agent:', command);
  nativePort.postMessage({
    type: 'command',
    command: command,
    tabId: command.tabId
  });
  
  return Promise.resolve();
}

// Handle action results from agent
async function handleActionResult(result) {
  console.log('✅ Action result:', result);
  
  if (result.action === 'navigate' && result.url) {
    // Update tab if needed
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    if (tabs.length > 0) {
      await browser.tabs.update(tabs[0].id, { url: result.url });
    }
  }
}

// Listen for messages from popup/sidebar
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('📨 Message from UI:', message);
  
  if (message.type === 'send-command') {
    // Get current tab info
    browser.tabs.query({ active: true, currentWindow: true })
      .then(tabs => {
        if (tabs.length > 0) {
          message.command.tabId = tabs[0].id;
          message.command.url = tabs[0].url;
        }
        return sendToAgent(message.command);
      })
      .then(() => {
        sendResponse({ success: true });
      })
      .catch(error => {
        sendResponse({ success: false, error: error.message });
      });
    
    return true; // Keep channel open for async response
  }
  
  if (message.type === 'check-agent-status') {
    sendResponse({ connected: agentConnected });
    return true;
  }
});

// Initialize
connectToAgent();

console.log('🚀 AgentXen background script loaded');
