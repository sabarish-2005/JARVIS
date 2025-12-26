import { useState, KeyboardEvent } from "react";
import { Send, Terminal } from "lucide-react";

interface CommandInputProps {
  onSubmit: (command: string) => void;
  disabled?: boolean;
}

const CommandInput = ({ onSubmit, disabled }: CommandInputProps) => {
  const [command, setCommand] = useState("");

  const handleSubmit = () => {
    if (command.trim() && !disabled) {
      onSubmit(command.trim());
      setCommand("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <div className="holo-panel p-4">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-primary/50">
          <Terminal className="w-4 h-4" />
          <span className="text-[10px] uppercase tracking-wider hidden sm:inline">CMD</span>
        </div>
        
        <div className="flex-1 relative">
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Enter command, sir..."
            className="
              w-full bg-background/50 border border-primary/20 rounded-lg
              px-4 py-3 text-sm text-primary placeholder-muted-foreground
              focus:outline-none focus:border-primary/50 focus:bg-background/80
              transition-all duration-300
              disabled:opacity-50
            "
            style={{
              boxShadow: "inset 0 0 20px hsl(195 100% 55% / 0.05)"
            }}
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-primary/30 animate-blink">
            █
          </div>
        </div>

        <button
          onClick={handleSubmit}
          disabled={!command.trim() || disabled}
          className="
            relative p-3 rounded-lg overflow-hidden
            border border-primary/30
            bg-primary/10 text-primary
            hover:bg-primary/20 hover:border-primary/50
            disabled:opacity-30 disabled:cursor-not-allowed
            transition-all duration-300
            group
          "
        >
          <div 
            className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity"
            style={{
              background: "radial-gradient(circle at center, hsl(195 100% 55% / 0.2), transparent 70%)"
            }}
          />
          <Send className="w-4 h-4 relative z-10" />
        </button>
      </div>
      
      {/* Typing indicator when processing */}
      {disabled && (
        <div className="flex items-center gap-2 mt-2 text-[10px] text-primary/60">
          <div className="flex gap-1">
            {[0, 1, 2].map((i) => (
              <div 
                key={i}
                className="w-1 h-1 rounded-full bg-primary animate-pulse"
                style={{ animationDelay: `${i * 0.2}s` }}
              />
            ))}
          </div>
          <span>Processing request...</span>
        </div>
      )}
    </div>
  );
};

export default CommandInput;