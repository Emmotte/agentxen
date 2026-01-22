/**
 * AgentXen Popup Script
 */

const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const openSidebarBtn = document.getElementById('open-sidebar');
const toggleAgentBtn = document.getElementById('toggle-agent-mode');

let agentMode = false;

// Check agent status
browser.runtime.sendMessage({ type: 'check-agent-status' })
  .then(response => {
    if (response.connected) {
      statusDot.classList.add('connected');
      statusText.textContent = 'Connected';
    } else {
      statusText.textContent = 'Disconnected';
    }
  });

// Open sidebar
openSidebarBtn.addEventListener('click', () => {
  browser.sidebarAction.open();
  window.close();
});

// Toggle agent mode for current tab
toggleAgentBtn.addEventListener('click', async () => {
  agentMode = !agentMode;
  toggleAgentBtn.textContent = agentMode ? 'Disable Agent Mode' : 'Enable Agent Mode';
  
  const tabs = await browser.tabs.query({ active: true, currentWindow: true });
  if (tabs.length > 0) {
    await browser.tabs.sendMessage(tabs[0].id, {
      type: 'set-agent-mode',
      enabled: agentMode
    });
  }
});
