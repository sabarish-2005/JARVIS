import { useState, useEffect } from "react";

interface BootSequenceProps {
  onComplete: () => void;
}

const bootMessages = [
  { text: "STARK INDUSTRIES SECURE BOOT v3.2.1", delay: 0, type: "system" },
  { text: "Initializing Arc Reactor Core...", delay: 400, type: "process" },
  { text: "Power Output: 3 GJ/s [OPTIMAL]", delay: 800, type: "status" },
  { text: "Loading J.A.R.V.I.S. Neural Matrix...", delay: 1200, type: "process" },
  { text: "Establishing Secure Uplink...", delay: 1600, type: "process" },
  { text: "Encryption: AES-512 [ACTIVE]", delay: 2000, type: "status" },
  { text: "Voice Recognition Calibrated", delay: 2400, type: "status" },
  { text: "HUD Systems Online", delay: 2800, type: "status" },
  { text: "All Systems Operational", delay: 3200, type: "success" },
  { text: "Good evening, Sir.", delay: 3800, type: "jarvis" },
];

const BootSequence = ({ onComplete }: BootSequenceProps) => {
  const [visibleMessages, setVisibleMessages] = useState<number[]>([]);
  const [showCursor, setShowCursor] = useState(true);
  const [progress, setProgress] = useState(0);
  const [reactorGlow, setReactorGlow] = useState(false);

  useEffect(() => {
    // Start reactor glow after a moment
    setTimeout(() => setReactorGlow(true), 500);

    bootMessages.forEach((msg, index) => {
      setTimeout(() => {
        setVisibleMessages((prev) => [...prev, index]);
        setProgress(((index + 1) / bootMessages.length) * 100);
      }, msg.delay);
    });

    const completeTimeout = setTimeout(() => {
      onComplete();
    }, 5000);

    const cursorInterval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 500);

    return () => {
      clearTimeout(completeTimeout);
      clearInterval(cursorInterval);
    };
  }, [onComplete]);

  const getMessageStyle = (type: string) => {
    switch (type) {
      case "system":
        return "text-primary/60";
      case "process":
        return "text-primary/80";
      case "status":
        return "text-secondary";
      case "success":
        return "text-primary arc-glow";
      case "jarvis":
        return "text-primary arc-glow text-base mt-2";
      default:
        return "text-primary/80";
    }
  };

  return (
    <div className="fixed inset-0 bg-background z-50 flex items-center justify-center overflow-hidden">
      {/* Background grid */}
      <div className="absolute inset-0 hud-grid opacity-50" />
      <div className="hud-scanline absolute inset-0 pointer-events-none" />

      {/* Ambient glow from center */}
      <div 
        className={`absolute w-96 h-96 rounded-full transition-all duration-2000 ${
          reactorGlow ? "opacity-40" : "opacity-0"
        }`}
        style={{
          background: "radial-gradient(circle, hsl(195 100% 55% / 0.3) 0%, transparent 70%)",
        }}
      />

      {/* Arc Reactor animation in center */}
      <div 
        className={`absolute transition-all duration-1000 ${
          reactorGlow ? "opacity-100 scale-100" : "opacity-0 scale-50"
        }`}
      >
        {/* Outer ring */}
        <div className="w-32 h-32 rounded-full border-2 border-primary/30 animate-rotate-slow flex items-center justify-center">
          {/* Middle ring */}
          <div className="w-24 h-24 rounded-full border border-primary/50 animate-rotate-reverse flex items-center justify-center">
            {/* Inner core */}
            <div 
              className="w-16 h-16 rounded-full animate-reactor-pulse"
              style={{
                background: `radial-gradient(circle, 
                  hsl(195 100% 90%) 0%, 
                  hsl(195 100% 60%) 40%, 
                  hsl(195 80% 40%) 70%, 
                  transparent 100%
                )`,
              }}
            />
          </div>
        </div>
      </div>

      <div className="relative max-w-2xl w-full mx-4 mt-48">
        {/* JARVIS Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-5xl font-bold arc-glow tracking-[0.4em] mb-2">
            J.A.R.V.I.S.
          </h1>
          <p className="text-[10px] md:text-xs text-muted-foreground tracking-[0.3em]">
            STARK INDUSTRIES • SECURE TERMINAL
          </p>
        </div>

        {/* Terminal Output */}
        <div className="holo-panel p-6 mb-6">
          <div className="font-mono text-xs space-y-1.5">
            {bootMessages.map((msg, index) => (
              <div
                key={index}
                className={`
                  flex items-center gap-2 transition-all duration-300
                  ${visibleMessages.includes(index) ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-4"}
                  ${getMessageStyle(msg.type)}
                `}
              >
                <span className="text-primary/40">▸</span>
                <span>{msg.text}</span>
                {index === visibleMessages.length - 1 && showCursor && (
                  <span className="text-primary ml-1">█</span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Progress Bar */}
        <div className="relative">
          <div className="h-1 bg-muted/30 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-500 ease-out arc-border-glow"
              style={{ 
                width: `${progress}%`,
                background: "linear-gradient(90deg, hsl(195 100% 55%), hsl(210 100% 70%))"
              }}
            />
          </div>
          <div className="flex justify-between mt-2 text-[10px] text-muted-foreground tracking-wider">
            <span>SYSTEM BOOT</span>
            <span>{Math.round(progress)}%</span>
          </div>
        </div>
      </div>

      {/* Corner decorations */}
      <div className="absolute top-8 left-8 w-20 h-20 border-l-2 border-t-2 border-primary/30" />
      <div className="absolute top-8 right-8 w-20 h-20 border-r-2 border-t-2 border-primary/30" />
      <div className="absolute bottom-8 left-8 w-20 h-20 border-l-2 border-b-2 border-primary/30" />
      <div className="absolute bottom-8 right-8 w-20 h-20 border-r-2 border-b-2 border-primary/30" />

      {/* Version info */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-[9px] text-primary/30 tracking-widest">
        JARVIS OS v4.7.2 • ARC REACTOR POWERED
      </div>
    </div>
  );
};

export default BootSequence;