import { useState, useCallback, Suspense, useEffect } from "react";
import BootSequence from "@/components/jarvis/BootSequence";
import JarvisHeader from "@/components/jarvis/JarvisHeader";
import ArcReactorCore from "@/components/jarvis/ArcReactorCore";
import SystemStats from "@/components/jarvis/SystemStats";
import VoicePanel from "@/components/jarvis/VoicePanel";
import ResponsePanel from "@/components/jarvis/ResponsePanel";
import CommandInput from "@/components/jarvis/CommandInput";
import RadialHUDRings from "@/components/jarvis/RadialHUDRings";
import HolographicModels from "@/components/jarvis/HolographicModels";
import { sendChatMessage, executeCommand, listenForVoice, speakText } from "@/services/api";
interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

const jarvisResponses = [
  "Right away, sir.",
  "Yes, sir. Processing your request.",
  "Certainly, sir. One moment.",
  "I shall look into that immediately, sir.",
  "At your service, sir.",
  "Consider it done, sir.",
  "Running diagnostics now, sir.",
  "I've prepared the necessary calculations, sir.",
  "The data you requested is now available, sir.",
  "Perhaps I can be of assistance, sir.",
  "I've taken the liberty of preparing several options, sir.",
  "All systems are functioning within normal parameters, sir.",
  "The Mark VII is ready for deployment, sir.",
  "Initiating protocol. Stand by, sir.",
];

const Index = () => {
  const [booting, setBooting] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [continuousMode, setContinuousMode] = useState(false);
  const [status, setStatus] = useState<"idle" | "listening" | "processing">("idle");

  const handleBootComplete = useCallback(() => {
    setBooting(false);
  }, []);

  const handleCommand = useCallback(async (command: string) => {
    console.log('🎤 User command received:', command);
    const userMessage: Message = {
      id: Date.now(),
      text: command,
      isUser: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setStatus("processing");

    try {
      // Try to execute as a command first
      console.log('⚡ Attempting to execute as command...');
      const commandResult = await executeCommand(command);
      
      let responseText: string;
      
      if (commandResult.success) {
        console.log('✅ Command executed successfully');
        responseText = commandResult.result?.message || "Command executed successfully, sir.";
      } else {
        // If command fails, try as a chat message
        console.log('💬 Command failed, trying as chat message...');
        const chatResult = await sendChatMessage(command);
        
        if (chatResult.success && chatResult.response) {
          console.log('✅ Chat response received');
          responseText = chatResult.response;
        } else {
          console.log('❌ Chat request failed:', chatResult.error);
          responseText = chatResult.error || "I apologize sir, but I encountered an issue processing your request.";
        }
      }
      
      const jarvisMessage: Message = {
        id: Date.now() + 1,
        text: responseText,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, jarvisMessage]);

      // Speak the response aloud when possible; wait until finished before resuming listening
      try {
        setIsSpeaking(true);
        await speakText(responseText);
      } catch (err) {
        console.warn("TTS failed", err);
      } finally {
        setIsSpeaking(false);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: "I apologize sir, but I'm currently unable to connect to my systems. Please ensure the backend server is running.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setStatus("idle");
    }
  }, []);

  const startContinuousListening = useCallback(() => {
    // If we're currently speaking, pause listening until speech finishes
    if (!continuousMode || isSpeaking) {
      if (continuousMode && isSpeaking) {
        setTimeout(() => startContinuousListening(), 500);
      }
      return;
    }
    
    setIsListening(true);
    
    // Listen for wake word or commands with longer timeout
    listenForVoice(15, true).then((result) => {
      if (!continuousMode) {
        setIsListening(false);
        return;
      }
      
      if (result.success && result.transcript) {
        const transcript = result.transcript.toLowerCase();
        console.log('🎤 Heard:', result.transcript);

        // Prefer wake-word path, but allow direct commands (e.g., "open calculator") to run without the wake word
        if (result.wake_word_detected || 
            transcript.includes('jarvis') || 
            transcript.includes('hey jarvis') || 
            transcript.includes('ok jarvis')) {
          console.log('🎯 Wake word detected!');

          // Remove wake word from command
          let command = result.transcript
            .replace(/hey jarvis/gi, '')
            .replace(/ok jarvis/gi, '')
            .replace(/jarvis/gi, '')
            .trim();

          if (command) {
            handleCommand(command);
          }
        } else if (transcript.length > 2) {
          // No wake word but actionable text detected; process directly for hands-free mode
          console.log('🧠 Processing command without wake word');
          handleCommand(result.transcript.trim());
        }
      } else if (result.error && result.error.includes('No audio detected')) {
        // Silently continue listening if no audio detected
        console.debug('🔇 No audio detected, continuing to listen...');
      } else if (result.error && (result.error.includes('Failed to fetch') || result.error.includes('Connection'))) {
        // Backend connection lost
        console.error('❌ Backend connection lost:', result.error);
        setContinuousMode(false);
        setIsListening(false);
        setStatus('idle');
        
        const errorMessage: Message = {
          id: Date.now(),
          text: "I apologize sir, but I've lost connection to my systems. Please restart the backend server.",
          isUser: false,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
        return;
      }
      
      // Continue listening if in continuous mode with a small delay
      if (continuousMode) {
        setTimeout(() => startContinuousListening(), 1000);
      } else {
        setIsListening(false);
      }
    }).catch((error) => {
      console.error("Continuous listening error:", error);
      if (continuousMode) {
        // Check if this is a connection error
        if (error.message?.includes('Failed to fetch') || error.message?.includes('Connection')) {
          console.error('❌ Backend is unreachable');
          setContinuousMode(false);
          setIsListening(false);
          setStatus('idle');
          
          const errorMessage: Message = {
            id: Date.now(),
            text: "Connection to backend lost. Please ensure the Flask server is running.",
            isUser: false,
            timestamp: new Date(),
          };
          setMessages((prev) => [...prev, errorMessage]);
          return;
        }
        // Add longer delay after errors
        setTimeout(() => startContinuousListening(), 2000);
      } else {
        setIsListening(false);
      }
    });
  }, [continuousMode, handleCommand, isSpeaking]);

  // Start continuous listening when mode is activated
  useEffect(() => {
    if (continuousMode) {
      startContinuousListening();
    }
    
    return () => {
      // Cleanup: stop listening if component unmounts or mode is disabled
      setIsListening(false);
    };
  }, [continuousMode, startContinuousListening]);

  const handleVoiceToggle = useCallback(() => {
    setContinuousMode((prev) => {
      const newMode = !prev;
      if (newMode) {
        console.log('🔊 Activating continuous listening mode (Siri-like)');
        setStatus("listening");
      } else {
        console.log('🔇 Deactivating continuous listening mode');
        setStatus("idle");
        setIsListening(false);
      }
      return newMode;
    });
  }, []);

  if (booting) {
    return <BootSequence onComplete={handleBootComplete} />;
  }

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden relative">
      {/* 3D Holographic Models Background */}
      <Suspense fallback={null}>
        <HolographicModels />
      </Suspense>

      {/* Background effects */}
      <div className="absolute inset-0 hud-grid" />
      <div className="hud-scanline fixed inset-0 pointer-events-none z-10" />
      
      {/* Radial HUD overlay */}
      <RadialHUDRings isActive={status !== "idle"} />

      {/* Header */}
      <JarvisHeader />

      {/* Main Content */}
      <main className="flex-1 flex flex-col lg:flex-row gap-4 p-4 overflow-hidden relative z-20">
        {/* Left Panel - System Stats & Voice */}
        <aside className="lg:w-64 flex flex-row lg:flex-col gap-4 animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
          <div className="flex-1 lg:flex-none">
            <SystemStats />
          </div>
          <div className="flex-1 lg:flex-none">
            <VoicePanel isListening={isListening} continuousMode={continuousMode} onToggle={handleVoiceToggle} />
          </div>
        </aside>

        {/* Center Panel - Arc Reactor Core */}
        <div className="flex-1 flex items-center justify-center min-h-[300px] lg:min-h-0 relative">
          <ArcReactorCore status={status} />
        </div>

        {/* Right Panel - Response Log */}
        <aside className="lg:w-80 h-64 lg:h-auto animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
          <ResponsePanel messages={messages} />
        </aside>
      </main>

      {/* Bottom Panel - Command Input */}
      <footer className="p-4 pt-0 relative z-20 animate-fade-in-up" style={{ animationDelay: "0.6s" }}>
        <CommandInput onSubmit={handleCommand} disabled={status === "processing"} />
      </footer>
    </div>
  );
};

export default Index;