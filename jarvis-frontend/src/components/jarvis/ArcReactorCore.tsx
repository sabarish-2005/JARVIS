import { useMemo } from "react";

interface ArcReactorCoreProps {
  status: "idle" | "listening" | "processing";
}

const ArcReactorCore = ({ status }: ArcReactorCoreProps) => {
  const isActive = status !== "idle";
  
  const statusText = useMemo(() => {
    switch (status) {
      case "listening":
        return "LISTENING...";
      case "processing":
        return "PROCESSING...";
      default:
        return "AWAITING COMMAND";
    }
  }, [status]);

  // Generate particle positions
  const particles = useMemo(() => 
    Array.from({ length: 12 }, (_, i) => ({
      id: i,
      angle: (i / 12) * 360,
      delay: i * 0.3,
      size: Math.random() * 3 + 2,
    })), []);

  return (
    <div className="relative flex items-center justify-center">
      {/* Outer ambient glow */}
      <div 
        className={`absolute w-[500px] h-[500px] rounded-full transition-opacity duration-1000 ${
          isActive ? "opacity-60" : "opacity-30"
        }`}
        style={{
          background: "radial-gradient(circle, hsl(195 100% 55% / 0.15) 0%, transparent 70%)",
        }}
      />

      {/* Outermost data ring with ticks */}
      <div 
        className="absolute w-[420px] h-[420px] rounded-full animate-rotate-slow ring-ticks-sparse"
        style={{ animationDuration: "60s" }}
      />

      {/* Outer rotating ring 1 - dashed */}
      <svg className="absolute w-[380px] h-[380px] animate-rotate-slow" style={{ animationDuration: "30s" }}>
        <circle
          cx="50%"
          cy="50%"
          r="48%"
          fill="none"
          stroke="hsl(195 100% 55%)"
          strokeWidth="1"
          strokeDasharray="8 20 2 20"
          opacity="0.4"
        />
      </svg>

      {/* Outer rotating ring 2 - markers */}
      <div 
        className="absolute w-[340px] h-[340px] rounded-full border border-primary/30 animate-rotate-reverse-slow"
        style={{ animationDuration: "45s" }}
      >
        {[0, 90, 180, 270].map((angle) => (
          <div
            key={angle}
            className="absolute w-2 h-2 bg-primary rounded-full"
            style={{
              top: "50%",
              left: "50%",
              transform: `rotate(${angle}deg) translateY(-170px) translateX(-50%)`,
            }}
          />
        ))}
      </div>

      {/* Data arc ring */}
      <svg className="absolute w-[300px] h-[300px] animate-rotate-medium" style={{ animationDuration: "20s" }}>
        <circle
          cx="50%"
          cy="50%"
          r="45%"
          fill="none"
          stroke="hsl(195 100% 70%)"
          strokeWidth="2"
          strokeDasharray="30 60 10 60"
          strokeLinecap="round"
          opacity="0.5"
        />
      </svg>

      {/* Secondary ring - reverse */}
      <svg className="absolute w-[260px] h-[260px] animate-rotate-reverse" style={{ animationDuration: "18s" }}>
        <circle
          cx="50%"
          cy="50%"
          r="45%"
          fill="none"
          stroke="hsl(210 100% 70%)"
          strokeWidth="1.5"
          strokeDasharray="20 40 5 40"
          opacity="0.4"
        />
      </svg>

      {/* Inner rotating ring with tick marks */}
      <div 
        className={`absolute w-[220px] h-[220px] rounded-full ring-ticks transition-all duration-500 ${
          isActive ? "animate-rotate-fast" : "animate-rotate-medium"
        }`}
        style={{ animationDuration: isActive ? "8s" : "15s" }}
      />

      {/* Core housing ring */}
      <div 
        className={`absolute w-[180px] h-[180px] rounded-full border-2 transition-all duration-500 ${
          isActive 
            ? "border-primary arc-border-glow-strong" 
            : "border-primary/60 arc-border-glow"
        }`}
      />

      {/* Inner core ring */}
      <div 
        className={`absolute w-[150px] h-[150px] rounded-full border transition-all duration-500 ${
          isActive ? "border-primary/80" : "border-primary/40"
        }`}
      />

      {/* Arc Reactor Core - Main glowing center */}
      <div 
        className={`absolute w-[120px] h-[120px] rounded-full transition-all duration-300 ${
          isActive ? "animate-reactor-active" : "animate-reactor-pulse"
        }`}
        style={{
          background: `radial-gradient(circle, 
            hsl(195 100% 95%) 0%, 
            hsl(195 100% 70%) 20%, 
            hsl(195 100% 55%) 40%, 
            hsl(195 80% 40%) 60%, 
            hsl(210 60% 20%) 80%, 
            transparent 100%
          )`,
        }}
      />

      {/* Core center bright spot */}
      <div 
        className="absolute w-[60px] h-[60px] rounded-full animate-pulse-glow"
        style={{
          background: `radial-gradient(circle, 
            hsl(195 100% 98%) 0%, 
            hsl(195 100% 80%) 40%, 
            transparent 70%
          )`,
        }}
      />

      {/* Triangular core segments */}
      <svg className="absolute w-[100px] h-[100px]" viewBox="0 0 100 100">
        {[0, 60, 120, 180, 240, 300].map((angle, i) => (
          <path
            key={i}
            d="M50,50 L50,20 L55,50 Z"
            fill="hsl(195 100% 90%)"
            opacity="0.8"
            transform={`rotate(${angle} 50 50)`}
          />
        ))}
      </svg>

      {/* Floating particles */}
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute w-1 h-1 rounded-full bg-primary animate-particle-float"
          style={{
            transform: `rotate(${particle.angle}deg) translateY(-100px)`,
            animationDelay: `${particle.delay}s`,
            width: particle.size,
            height: particle.size,
            opacity: 0.6,
          }}
        />
      ))}

      {/* Radar sweep overlay */}
      <div 
        className={`absolute w-[180px] h-[180px] rounded-full radar-sweep transition-opacity duration-500 ${
          isActive ? "opacity-40" : "opacity-20"
        }`}
        style={{ animationDuration: isActive ? "2s" : "4s" }}
      />

      {/* Status text display */}
      <div className="absolute bottom-[-80px] text-center">
        <div 
          className={`text-xs tracking-[0.3em] transition-all duration-500 ${
            isActive ? "text-primary arc-glow" : "text-primary/70 arc-glow-subtle"
          }`}
        >
          {statusText}
        </div>
        <div className="mt-2 flex justify-center gap-1">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                isActive ? "bg-primary" : "bg-primary/40"
              }`}
              style={{
                animationDelay: `${i * 0.2}s`,
                animation: isActive ? "pulse-glow 1s ease-in-out infinite" : "none",
              }}
            />
          ))}
        </div>
      </div>

      {/* Corner HUD elements */}
      <div className="absolute -top-4 -left-4 w-8 h-8 border-l-2 border-t-2 border-primary/40" />
      <div className="absolute -top-4 -right-4 w-8 h-8 border-r-2 border-t-2 border-primary/40" />
      <div className="absolute -bottom-4 -left-4 w-8 h-8 border-l-2 border-b-2 border-primary/40" />
      <div className="absolute -bottom-4 -right-4 w-8 h-8 border-r-2 border-b-2 border-primary/40" />
    </div>
  );
};

export default ArcReactorCore;