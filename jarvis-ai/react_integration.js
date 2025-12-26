/**
 * Example React Hooks for JARVIS API Integration
 * This file provides reusable React components and hooks
 */

import axios from 'axios';
import { useState, useCallback, useRef, useEffect } from 'react';

// ==================== CONFIGURATION ====================

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with timeout
const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== CUSTOM HOOKS ====================

/**
 * Hook for API requests with loading and error states
 */
export const useJarvisAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (method, endpoint, data = null) => {
    setLoading(true);
    setError(null);
    try {
      const config = { method, url: endpoint };
      if (data) config.data = data;
      
      const response = await api(config);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { request, loading, error };
};

/**
 * Hook for chat functionality
 */
export const useJarvisChat = () => {
  const { request, loading, error } = useJarvisAPI();
  const [messages, setMessages] = useState([]);

  const sendMessage = useCallback(async (message) => {
    if (!message.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    try {
      const data = await request('POST', '/chat', { message });
      
      // Add AI response
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      
      return data.response;
    } catch (err) {
      setMessages(prev => [...prev, { role: 'system', content: `Error: ${error}` }]);
      throw err;
    }
  }, [request, error]);

  const clearChat = useCallback(() => {
    setMessages([]);
  }, []);

  return { messages, sendMessage, clearChat, loading, error };
};

/**
 * Hook for voice interaction
 */
export const useJarvisVoice = () => {
  const { request, loading, error } = useJarvisAPI();
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');

  const listen = useCallback(async (duration = 5) => {
    setIsListening(true);
    setTranscript('');
    try {
      const data = await request('POST', '/listen', { duration });
      setTranscript(data.transcript);
      return data.transcript;
    } finally {
      setIsListening(false);
    }
  }, [request]);

  const speak = useCallback(async (text) => {
    try {
      await request('POST', '/speak', { text });
    } catch (err) {
      console.error('Speech error:', err);
      throw err;
    }
  }, [request]);

  return { listen, speak, isListening, transcript, error, loading };
};

/**
 * Hook for executing commands
 */
export const useJarvisCommand = () => {
  const { request, loading, error } = useJarvisAPI();

  const execute = useCallback(async (command) => {
    try {
      const data = await request('POST', '/command', { command });
      return data;
    } catch (err) {
      throw err;
    }
  }, [request]);

  const parseCommand = useCallback(async (command) => {
    try {
      const data = await request('POST', '/parse', { command });
      return data.intent;
    } catch (err) {
      throw err;
    }
  }, [request]);

  return { execute, parseCommand, loading, error };
};

/**
 * Hook for system control
 */
export const useJarvisSystem = () => {
  const { request, loading, error } = useJarvisAPI();

  const controlVolume = useCallback(async (action, level = null) => {
    const data = { action };
    if (level !== null) data.level = level;
    return request('POST', '/system/volume', data);
  }, [request]);

  const takeScreenshot = useCallback(() => {
    return request('POST', '/system/screenshot', {});
  }, [request]);

  const lock = useCallback(() => {
    return request('POST', '/system/lock', {});
  }, [request]);

  const shutdown = useCallback((delay = 0) => {
    return request('POST', '/system/shutdown', { delay });
  }, [request]);

  const restart = useCallback(() => {
    return request('POST', '/system/restart', {});
  }, [request]);

  const getTime = useCallback(() => {
    return request('GET', '/time');
  }, [request]);

  const getDate = useCallback(() => {
    return request('GET', '/date');
  }, [request]);

  return {
    controlVolume,
    takeScreenshot,
    lock,
    shutdown,
    restart,
    getTime,
    getDate,
    loading,
    error,
  };
};

/**
 * Hook for browser control
 */
export const useJarvisBrowser = () => {
  const { request, loading, error } = useJarvisAPI();

  const youtubeSearch = useCallback(async (query) => {
    return request('POST', '/browser/youtube', { query });
  }, [request]);

  const googleSearch = useCallback(async (query) => {
    return request('POST', '/browser/google', { query });
  }, [request]);

  return { youtubeSearch, googleSearch, loading, error };
};

/**
 * Hook to fetch supported actions
 */
export const useJarvisActions = () => {
  const { request } = useJarvisAPI();
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchActions = async () => {
      setLoading(true);
      try {
        const data = await request('GET', '/actions');
        setActions(data.actions);
      } catch (err) {
        console.error('Error fetching actions:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchActions();
  }, [request]);

  return { actions, loading };
};

/**
 * Hook for API health check
 */
export const useJarvisHealth = () => {
  const { request } = useJarvisAPI();
  const [status, setStatus] = useState(null);
  const [isHealthy, setIsHealthy] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await request('GET', '/health');
        setStatus(data);
        setIsHealthy(true);
      } catch (err) {
        setIsHealthy(false);
      }
    };

    checkHealth();
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, [request]);

  return { status, isHealthy };
};

// ==================== EXAMPLE COMPONENTS ====================

/**
 * Example Chat Component
 */
export const JarvisChatComponent = () => {
  const { messages, sendMessage, clearChat, loading } = useJarvisChat();
  const [input, setInput] = useState('');

  const handleSend = async () => {
    await sendMessage(input);
    setInput('');
  };

  return (
    <div className="jarvis-chat">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-group">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask JARVIS..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
        <button onClick={clearChat}>Clear</button>
      </div>
    </div>
  );
};

/**
 * Example Voice Control Component
 */
export const JarvisVoiceComponent = () => {
  const { listen, speak, isListening, transcript } = useJarvisVoice();
  const { execute } = useJarvisCommand();

  const handleListen = async () => {
    try {
      const result = await listen(5);
      console.log('Heard:', result);
      // Optionally execute the heard command
      if (result) {
        await execute(result);
      }
    } catch (err) {
      console.error('Listen error:', err);
    }
  };

  const handleSpeak = async () => {
    await speak('Hello! I am JARVIS, your AI assistant.');
  };

  return (
    <div className="jarvis-voice">
      <button onClick={handleListen} disabled={isListening}>
        {isListening ? 'Listening...' : 'Listen'}
      </button>
      <button onClick={handleSpeak}>Speak</button>
      {transcript && <p>Heard: {transcript}</p>}
    </div>
  );
};

/**
 * Example System Control Component
 */
export const JarvisSystemComponent = () => {
  const { controlVolume, takeScreenshot, getTime, getDate } = useJarvisSystem();
  const [currentTime, setCurrentTime] = useState('');
  const [currentDate, setCurrentDate] = useState('');

  const handleGetTime = async () => {
    const data = await getTime();
    setCurrentTime(data.result.message);
  };

  const handleGetDate = async () => {
    const data = await getDate();
    setCurrentDate(data.result.message);
  };

  return (
    <div className="jarvis-system">
      <button onClick={() => controlVolume('up')}>Volume Up</button>
      <button onClick={() => controlVolume('down')}>Volume Down</button>
      <button onClick={() => controlVolume('mute')}>Mute</button>
      <button onClick={takeScreenshot}>Screenshot</button>
      <button onClick={handleGetTime}>Get Time</button>
      <button onClick={handleGetDate}>Get Date</button>
      {currentTime && <p>Time: {currentTime}</p>}
      {currentDate && <p>Date: {currentDate}</p>}
    </div>
  );
};

// ==================== EXPORT ====================

export default {
  useJarvisAPI,
  useJarvisChat,
  useJarvisVoice,
  useJarvisCommand,
  useJarvisSystem,
  useJarvisBrowser,
  useJarvisActions,
  useJarvisHealth,
  JarvisChatComponent,
  JarvisVoiceComponent,
  JarvisSystemComponent,
};
