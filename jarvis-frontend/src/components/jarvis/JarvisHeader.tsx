import { useState, useEffect } from "react";

const JarvisHeader = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="relative flex items-center justify-between px-6 py-4 border-b border-primary/20">
      {/* Left section - Status */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="relative">
            <div className="w-3 h-3 rounded-full bg-primary animate-pulse-glow" />
            <div className="absolute inset-0 w-3 h-3 rounded-full bg-primary/50 animate-ping" />
          </div>
          <span className="text-[10px] text-primary/80 uppercase tracking-widest">System Online</span>
        </div>
        
        <div className="hidden md:flex items-center gap-4 text-[9px] text-muted-foreground">
          <span className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-secondary/60" />
            SECURE
          </span>
          <span className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-secondary/60" />
            ENCRYPTED
          </span>
        </div>
      </div>

      {/* Center - Title */}
      <div className="absolute left-1/2 -translate-x-1/2 text-center">
        <h1 className="text-xl md:text-2xl font-bold arc-glow tracking-[0.3em]">
          J.A.R.V.I.S.
        </h1>
        <p className="text-[8px] md:text-[9px] text-muted-foreground tracking-[0.2em] mt-0.5">
          STARK INDUSTRIES INTERFACE
        </p>
      </div>

      {/* Right section - Time */}
      <div className="text-right">
        <div className="text-sm md:text-base font-medium text-primary arc-glow-subtle tabular-nums">
          {time.toLocaleTimeString("en-US", { hour12: false })}
        </div>
        <div className="text-[9px] text-muted-foreground tracking-wider">
          {time.toLocaleDateString("en-US", { 
            weekday: "short", 
            month: "short", 
            day: "numeric",
            year: "numeric"
          }).toUpperCase()}
        </div>
      </div>

      {/* Decorative line under header */}
      <div 
        className="absolute bottom-0 left-1/2 -translate-x-1/2 h-px w-1/3"
        style={{
          background: "linear-gradient(90deg, transparent, hsl(195 100% 55% / 0.5), transparent)"
        }}
      />
    </header>
  );
};

export default JarvisHeader;