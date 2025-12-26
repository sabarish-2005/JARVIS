import { Mic } from "lucide-react";
import { useEffect, useState } from "react";

interface VoicePanelProps {
  isListening: boolean;
  continuousMode?: boolean;
  onToggle: () => void;
}

const VoicePanel = ({ isListening, continuousMode = false, onToggle }: VoicePanelProps) => {
  const [waveformHeights, setWaveformHeights] = useState<number[]>(
    Array(16).fill(4)
  );

  useEffect(() => {
    if (!isListening) {
      setWaveformHeights(Array(16).fill(4));
      return;
    }

    const interval = setInterval(() => {
      setWaveformHeights(
        Array(16).fill(0).map(() => Math.random() * 28 + 4)
      );
    }, 100);

    return () => clearInterval(interval);
  }, [isListening]);

  return (
    <div className="holo-panel p-4">
      <div className="flex items-center justify-between border-b border-primary/20 pb-2 mb-4">
        <h3 className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
          Voice Interface
        </h3>
        <span className={`text-[8px] uppercase tracking-wider ${continuousMode ? "text-primary animate-pulse" : isListening ? "text-primary" : "text-muted-foreground"}`}>
          {continuousMode ? "CONTINUOUS" : isListening ? "ACTIVE" : "STANDBY"}
        </span>
      </div>
      
      <div className="flex flex-col items-center gap-4">
        {/* Microphone button with arc reactor style */}
        <button
          onClick={onToggle}
          className={`
            relative w-16 h-16 rounded-full transition-all duration-300
            flex items-center justify-center
            ${continuousMode
              ? "bg-primary/30 arc-border-glow-strong shadow-lg shadow-primary/50" 
              : isListening 
              ? "bg-primary/20 arc-border-glow-strong" 
              : "bg-transparent hover:bg-primary/10"
            }
          `}
        >
          {/* Outer ring */}
          <div className={`
            absolute inset-0 rounded-full border-2 transition-all duration-300
            ${continuousMode ? "border-primary animate-pulse" : isListening ? "border-primary" : "border-primary/30"}
          `} />
          
          {/* Inner ring */}
          <div className={`
            absolute inset-2 rounded-full border transition-all duration-300
            ${isListening ? "border-primary/60" : "border-primary/20"}
          `} />
          
          <Mic className={`w-5 h-5 relative z-10 transition-colors ${
            continuousMode ? "text-primary animate-pulse" : isListening ? "text-primary" : "text-primary/50"
          }`} />
          
          {(isListening || continuousMode) && (
            <>
              <div className="absolute inset-0 rounded-full border-2 border-primary animate-ping opacity-30" />
              <div 
                className="absolute inset-0 rounded-full animate-pulse"
                style={{
                  background: "radial-gradient(circle, hsl(195 100% 55% / 0.2) 0%, transparent 70%)"
                }}
              />
            </>
          )}
        </button>
        
        <div className="text-center">
          <span className="text-[10px] text-muted-foreground uppercase tracking-wider block">
            {continuousMode ? "Say 'Hey Jarvis'" : isListening ? "Listening..." : "Tap for Continuous Mode"}
          </span>
          {continuousMode && (
            <span className="text-[8px] text-primary/60 block mt-1">
              Always listening for wake word
            </span>
          )}
        </div>

        {/* Voice waveform visualization */}
        <div className="flex items-end justify-center gap-0.5 h-8 w-full">
          {waveformHeights.map((height, i) => (
            <div
              key={i}
              className="w-1 rounded-full transition-all duration-100"
              style={{
                height: `${height}px`,
                background: isListening 
                  ? `linear-gradient(180deg, hsl(195 100% 70%), hsl(195 100% 50%))` 
                  : "hsl(195 100% 50% / 0.3)",
                boxShadow: isListening ? "0 0 4px hsl(195 100% 55% / 0.5)" : "none"
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default VoicePanel;