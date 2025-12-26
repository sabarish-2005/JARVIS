interface HoloPanel {
  id: string;
  title: string;
  content: React.ReactNode;
  position: "left" | "right";
  delay?: number;
}

interface FloatingHoloPanelProps {
  title: string;
  children: React.ReactNode;
  position: "left" | "right";
  delay?: number;
  className?: string;
}

const FloatingHoloPanel = ({ 
  title, 
  children, 
  position, 
  delay = 0,
  className = ""
}: FloatingHoloPanelProps) => {
  return (
    <div 
      className={`
        holo-panel-floating p-4 animate-fade-in-up
        ${position === "left" ? "mr-auto" : "ml-auto"}
        ${className}
      `}
      style={{ 
        animationDelay: `${delay}s`,
        animationFillMode: "backwards"
      }}
    >
      {/* Panel header with connection line */}
      <div className="relative mb-3">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
          <h3 className="text-[10px] uppercase tracking-[0.2em] text-primary/80">
            {title}
          </h3>
        </div>
        
        {/* Connection line to core */}
        <div 
          className={`absolute top-1/2 h-px bg-gradient-to-r ${
            position === "left" 
              ? "left-full w-12 from-primary/40 to-transparent ml-2" 
              : "right-full w-12 from-transparent to-primary/40 mr-2"
          }`}
        />
      </div>

      {/* Panel content */}
      <div className="text-xs text-primary/90">
        {children}
      </div>

      {/* Decorative corner accents */}
      <div className="absolute top-0 left-0 w-3 h-3 border-l border-t border-primary/50" />
      <div className="absolute top-0 right-0 w-3 h-3 border-r border-t border-primary/50" />
      <div className="absolute bottom-0 left-0 w-3 h-3 border-l border-b border-primary/50" />
      <div className="absolute bottom-0 right-0 w-3 h-3 border-r border-b border-primary/50" />
    </div>
  );
};

export default FloatingHoloPanel;