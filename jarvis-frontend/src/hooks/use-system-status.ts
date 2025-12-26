import { useState, useEffect } from 'react';
import { checkHealth, getSystemStatus } from '@/services/api';

interface SystemStatus {
  isConnected: boolean;
  isHealthy: boolean;
  components?: {
    voice_engine: string;
    intent_parser: string;
    action_executor: string;
    ai_brain: string;
  };
}

/**
 * Hook to monitor the JARVIS backend connection status
 */
export function useSystemStatus(checkInterval: number = 10000) {
  const [status, setStatus] = useState<SystemStatus>({
    isConnected: false,
    isHealthy: false,
  });

  useEffect(() => {
    const checkStatus = async () => {
      console.log('🔄 Checking backend connection status...');
      try {
        const healthy = await checkHealth();
        
        if (healthy) {
          const sysStatus = await getSystemStatus();
          console.log('✅ Backend connected and healthy');
          setStatus({
            isConnected: true,
            isHealthy: true,
            components: sysStatus?.components,
          });
        } else {
          console.warn('⚠️ Backend health check failed');
          setStatus({
            isConnected: false,
            isHealthy: false,
          });
        }
      } catch (error) {
        console.error('❌ Backend connection error:', error);
        setStatus({
          isConnected: false,
          isHealthy: false,
        });
      }
    };

    // Check immediately
    console.log('🚀 Starting system status monitoring...');
    checkStatus();

    // Then check periodically
    const interval = setInterval(checkStatus, checkInterval);

    return () => clearInterval(interval);
  }, [checkInterval]);

  return status;
}
