/**
 * AgentXen Content Script
 * Injected into web pages to enable agent interaction
 */

// Mark tabs controlled by agent
let agentControlled = false;

// Listen for messages from background script
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'set-agent-mode') {
    agentControlled = message.enabled;
    updatePageIndicator();
    sendResponse({ success: true });
  }
  
  if (message.type === 'execute-action') {
    executeAction(message.action)
      .then(result => sendResponse({ success: true, result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Async response
  }
});

// Execute agent actions on page
async function executeAction(action) {
  console.log('⚡ Executing action:', action);
  
  switch (action.type) {
    case 'click':
      const clickEl = document.querySelector(action.selector);
      if (clickEl) {
        clickEl.click();
        return { clicked: action.selector };
      }
      throw new Error(`Element not found: ${action.selector}`);
      
    case 'type':
      const typeEl = document.querySelector(action.selector);
      if (typeEl) {
        typeEl.value = action.text;
        typeEl.dispatchEvent(new Event('input', { bubbles: true }));
        return { typed: action.text };
      }
      throw new Error(`Element not found: ${action.selector}`);
      
    case 'extract':
      const extractEl = document.querySelector(action.selector || 'body');
      if (extractEl) {
        return { text: extractEl.textContent.trim().substring(0, 1000) };
      }
      throw new Error(`Element not found: ${action.selector}`);
      
    case 'scroll':
      window.scrollBy(0, action.amount || 300);
      return { scrolled: action.amount || 300 };
      
    default:
      throw new Error(`Unknown action type: ${action.type}`);
  }
}

// Visual indicator when page is agent-controlled
function updatePageIndicator() {
  let indicator = document.getElementById('agentxen-indicator');
  
  if (agentControlled && !indicator) {
    indicator = document.createElement('div');
    indicator.id = 'agentxen-indicator';
    indicator.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: #0084ff;
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      z-index: 999999;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    `;
    indicator.textContent = '🤖 Agent Mode';
    document.body.appendChild(indicator);
  } else if (!agentControlled && indicator) {
    indicator.remove();
  }
}

console.log('🚀 AgentXen content script loaded');
