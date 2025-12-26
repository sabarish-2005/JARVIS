/**
 * JARVIS API Service
 * Handles all communication with the Flask backend
 */

// When served from Flask, use relative URL. Otherwise use localhost:5000
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (window.location.port === '5000' ? '' : 'http://localhost:5000');

// Log API configuration on startup
console.log('🤖 JARVIS API Service Initialized');
console.log('🌐 API Base URL:', API_BASE_URL || '(relative - same origin)');
console.log('📋 Available endpoints:');
console.log('  - GET  /api/health');
console.log('  - GET  /api/status');
console.log('  - POST /api/chat');
console.log('  - POST /api/command');
console.log('  - POST /api/listen');
console.log('  - POST /api/speak');

export interface ChatResponse {
  success: boolean;
  message?: string;
  response?: string;
  error?: string;
  timestamp?: string;
}

export interface CommandResponse {
  success: boolean;
  command?: string;
  action?: string;
  result?: any;
  error?: string;
  timestamp?: string;
}

export interface StatusResponse {
  status: string;
  components: {
    voice_engine: string;
    intent_parser: string;
    action_executor: string;
    ai_brain: string;
  };
  wake_word: string;
  timestamp: string;
}

export interface VoiceListenResponse {
  success: boolean;
  transcript?: string;
  wake_word_detected?: boolean;
  error?: string;
  timestamp?: string;
}

export interface VoiceSpeakResponse {
  success: boolean;
  text?: string;
  error?: string;
  timestamp?: string;
}

/**
 * Send a chat message to JARVIS AI
 */
export async function sendChatMessage(message: string): Promise<ChatResponse> {
  console.log('📤 Sending chat message:', message);
  console.log('🌐 API URL:', `${API_BASE_URL}/api/chat`);
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    console.log('📥 Response status:', response.status, response.statusText);
    const data = await response.json();
    console.log('📥 Chat response:', data);
    return data;
  } catch (error) {
    console.error('❌ Chat API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to connect to JARVIS',
    };
  }
}

/**
 * Execute a JARVIS command
 */
export async function executeCommand(command: string): Promise<CommandResponse> {
  console.log('⚡ Executing command:', command);
  console.log('🌐 API URL:', `${API_BASE_URL}/api/command`);
  try {
    const response = await fetch(`${API_BASE_URL}/api/command`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command }),
    });

    console.log('📥 Response status:', response.status, response.statusText);
    const data = await response.json();
    console.log('📥 Command response:', data);
    return data;
  } catch (error) {
    console.error('❌ Command API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to execute command',
    };
  }
}

/**
 * Get JARVIS system status
 */
export async function getSystemStatus(): Promise<StatusResponse | null> {
  console.log('🔍 Getting system status:', `${API_BASE_URL}/api/status`);
  try {
    const response = await fetch(`${API_BASE_URL}/api/status`);
    const data = await response.json();
    console.log('🔍 System status:', data);
    return data;
  } catch (error) {
    console.error('❌ Status API error:', error);
    return null;
  }
}

/**
 * Check if API server is healthy
 */
export async function checkHealth(): Promise<boolean> {
  console.log('💓 Checking API health:', `${API_BASE_URL}/api/health`);
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    const data = await response.json();
    const isHealthy = data.status === 'online';
    console.log('💓 Health check result:', isHealthy ? '✅ Online' : '❌ Offline');
    return isHealthy;
  } catch (error) {
    console.error('❌ Health check failed:', error);
    return false;
  }
}

/**
 * Listen for voice input
 */
export async function listenForVoice(duration: number = 5, wakeWordMode: boolean = false): Promise<VoiceListenResponse> {
  console.log('🎤 Requesting voice input (duration:', duration, 'seconds, wake word mode:', wakeWordMode, ')');
  console.log('🌐 API URL:', `${API_BASE_URL}/api/listen`);
  try {
    const response = await fetch(`${API_BASE_URL}/api/listen`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ duration, wake_word: wakeWordMode }),
    });

    console.log('📥 Response status:', response.status, response.statusText);
    const data = await response.json();
    
    if (response.status === 503) {
      console.warn('⚠️ Voice recognition not available on backend');
    } else if (!data.success) {
      if (data.error?.includes('No audio detected')) {
        console.log('🔇 No audio detected during listen attempt');
      } else {
        console.error('❌ Voice listen failed:', data.error);
      }
    } else {
      console.log('✅ Voice transcript:', data.transcript);
    }
    
    return data;
  } catch (error) {
    console.error('❌ Voice listen API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to listen',
    };
  }
}

/**
 * Convert text to speech
 */
export async function speakText(text: string): Promise<VoiceSpeakResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/speak`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Voice speak API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to speak',
    };
  }
}

/**
 * System stats response interface
 */
export interface SystemStatsResponse {
  success: boolean;
  cpu?: {
    percent: number;
    cores: number;
  };
  memory?: {
    percent: number;
    total_gb: number;
    used_gb: number;
  };
  disk?: {
    percent: number;
    total_gb: number;
    used_gb: number;
  };
  battery?: {
    percent: number;
    charging: boolean;
  } | null;
  network?: {
    sent_mb: number;
    recv_mb: number;
  };
  error?: string;
  timestamp?: string;
}

/**
 * Get live system statistics
 */
export async function getSystemStats(): Promise<SystemStatsResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/system-stats`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('System stats API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to get stats',
    };
  }
}
