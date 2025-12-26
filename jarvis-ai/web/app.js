const API_BASE = '/api';

const statusEl = document.getElementById('status');
const chatLog = document.getElementById('chat-log');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const cmdInput = document.getElementById('cmd-input');
const cmdRun = document.getElementById('cmd-run');
const cmdOutput = document.getElementById('cmd-output');
const actionsOutput = document.getElementById('actions-output');
const actionsList = document.getElementById('actions-list');

function addChat(role, text) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.textContent = `${role === 'user' ? 'You' : 'JARVIS'}: ${text}`;
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  return res.json();
}

async function checkHealth() {
  statusEl.textContent = 'Checking...';
  try {
    const data = await fetchJSON(`${API_BASE}/health`);
    statusEl.textContent = data.status === 'online' ? 'Online' : 'Degraded';
  } catch (e) {
    statusEl.textContent = 'Offline';
  }
}

async function loadActions() {
  try {
    const data = await fetchJSON(`${API_BASE}/actions`);
    actionsList.innerHTML = '';
    (data.actions || []).forEach(name => {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = name;
      actionsList.appendChild(chip);
    });
  } catch (e) {
    // ignore
  }
}

async function sendChat() {
  const msg = chatInput.value.trim();
  if (!msg) return;
  chatInput.value = '';
  addChat('user', msg);
  try {
    const data = await fetchJSON(`${API_BASE}/chat`, {
      method: 'POST',
      body: JSON.stringify({ message: msg })
    });
    addChat('bot', data.response || 'No response');
  } catch (e) {
    addChat('bot', 'Error talking to server');
  }
}

async function runCommand(cmd) {
  cmdOutput.textContent = 'Running...';
  try {
    const data = await fetchJSON(`${API_BASE}/command`, {
      method: 'POST',
      body: JSON.stringify({ command: cmd })
    });
    cmdOutput.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    cmdOutput.textContent = 'Error running command';
  }
}

async function quickAction(action) {
  actionsOutput.textContent = 'Running...';
  try {
    if (action === 'time') {
      const data = await fetchJSON(`${API_BASE}/time`);
      actionsOutput.textContent = JSON.stringify(data, null, 2);
      return;
    }
    if (action === 'date') {
      const data = await fetchJSON(`${API_BASE}/date`);
      actionsOutput.textContent = JSON.stringify(data, null, 2);
      return;
    }
    // Fall back to command
    const data = await fetchJSON(`${API_BASE}/command`, {
      method: 'POST',
      body: JSON.stringify({ command: action.replace('_', ' ') })
    });
    actionsOutput.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    actionsOutput.textContent = 'Error';
  }
}

chatSend.onclick = sendChat;
chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendChat();
});

cmdRun.onclick = () => {
  const cmd = cmdInput.value.trim();
  if (!cmd) return;
  runCommand(cmd);
};

Array.from(document.querySelectorAll('.actions button')).forEach(btn => {
  btn.onclick = () => quickAction(btn.dataset.action);
});

checkHealth();
loadActions();
