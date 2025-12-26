import { useEffect, useState } from "react";

interface RadialHUDRingsProps {
  isActive?: boolean;
}

const RadialHUDRings = ({ isActive = false }: RadialHUDRingsProps) => {
  const [glitchActive, setGlitchActive] = useState(false);

  // Occasional glitch effect
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() > 0.95) {
        setGlitchActive(true);
        setTimeout(() => setGlitchActive(false), 150);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`absolute inset-0 pointer-events-none ${glitchActive ? "animate-glitch" : ""}`}>
      {/* Outermost decorative ring */}
      <svg className="absolute inset-0 w-full h-full opacity-20">
        <defs>
          <radialGradient id="ringGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="transparent" />
            <stop offset="85%" stopColor="transparent" />
            <stop offset="90%" stopColor="hsl(195, 100%, 55%)" stopOpacity="0.3" />
            <stop offset="95%" stopColor="hsl(195, 100%, 55%)" stopOpacity="0.1" />
            <stop offset="100%" stopColor="transparent" />
          </radialGradient>
        </defs>
        <circle cx="50%" cy="50%" r="48%" fill="url(#ringGradient)" />
      </svg>

      {/* Horizontal scan line */}
      <div 
        className="absolute left-0 right-0 h-px scan-line-horizontal"
        style={{ top: "50%" }}
      />

      {/* Corner HUD brackets - top left */}
      <div className="absolute top-8 left-8">
        <div className="w-24 h-24 border-l-2 border-t-2 border-primary/30" />
        <div className="absolute top-2 left-2 w-16 h-16 border-l border-t border-primary/20" />
        <div className="absolute top-4 left-4 text-[8px] text-primary/50 tracking-widest">
          HUD-01
        </div>
      </div>

      {/* Corner HUD brackets - top right */}
      <div className="absolute top-8 right-8">
        <div className="w-24 h-24 border-r-2 border-t-2 border-primary/30" />
        <div className="absolute top-2 right-2 w-16 h-16 border-r border-t border-primary/20" />
        <div className="absolute top-4 right-4 text-[8px] text-primary/50 tracking-widest text-right">
          SYS-OK
        </div>
      </div>

      {/* Corner HUD brackets - bottom left */}
      <div className="absolute bottom-8 left-8">
        <div className="w-24 h-24 border-l-2 border-b-2 border-primary/30" />
        <div className="absolute bottom-2 left-2 w-16 h-16 border-l border-b border-primary/20" />
      </div>

      {/* Corner HUD brackets - bottom right */}
      <div className="absolute bottom-8 right-8">
        <div className="w-24 h-24 border-r-2 border-b-2 border-primary/30" />
        <div className="absolute bottom-2 right-2 w-16 h-16 border-r border-b border-primary/20" />
      </div>

      {/* Side data bars - left */}
      <div className="absolute left-4 top-1/2 -translate-y-1/2 space-y-1">
        {[...Array(8)].map((_, i) => (
          <div 
            key={i}
            className="h-1 bg-primary/20 rounded-full animate-pulse"
            style={{ 
              width: `${20 + Math.random() * 30}px`,
              animationDelay: `${i * 0.2}s`
            }}
          />
        ))}
      </div>

      {/* Side data bars - right */}
      <div className="absolute right-4 top-1/2 -translate-y-1/2 space-y-1 flex flex-col items-end">
        {[...Array(8)].map((_, i) => (
          <div 
            key={i}
            className="h-1 bg-primary/20 rounded-full animate-pulse"
            style={{ 
              width: `${20 + Math.random() * 30}px`,
              animationDelay: `${i * 0.15}s`
            }}
          />
        ))}
      </div>

      {/* Circular reticle marks */}
      <svg className="absolute inset-0 w-full h-full">
        <g transform="translate(50%, 50%)">
          {[0, 45, 90, 135, 180, 225, 270, 315].map((angle) => (
            <line
              key={angle}
              x1="0"
              y1="-42%"
              x2="0"
              y2="-45%"
              stroke="hsl(195, 100%, 55%)"
              strokeWidth="1"
              opacity="0.4"
              transform={`rotate(${angle})`}
            />
          ))}
        </g>
      </svg>

      {/* Data readout overlays */}
      <div className="absolute top-1/4 left-12 text-[9px] text-primary/40 tracking-wider">
        <div>LAT: 40.7128°</div>
        <div>LNG: -74.0060°</div>
      </div>

      <div className="absolute top-1/4 right-12 text-[9px] text-primary/40 tracking-wider text-right">
        <div>ALT: 256M</div>
        <div>SPD: 0 M/S</div>
      </div>

      {/* Bottom center status */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4 text-[9px] text-primary/40">
        <span>STARK INDUSTRIES</span>
        <div className="w-2 h-2 rounded-full bg-primary/40 animate-pulse" />
        <span>SECURE CHANNEL</span>
      </div>
    </div>
  );
};

export default RadialHUDRings;