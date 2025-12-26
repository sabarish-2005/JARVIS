import { useRef, useEffect } from "react";

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface ResponsePanelProps {
  messages: Message[];
}

const ResponsePanel = ({ messages }: ResponsePanelProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="holo-panel p-4 h-full flex flex-col">
      <div className="flex items-center justify-between border-b border-primary/20 pb-2 mb-4">
        <h3 className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
          Communication Log
        </h3>
        <div className="flex items-center gap-1">
          <div className="w-1.5 h-1.5 rounded-full bg-secondary/60" />
          <span className="text-[8px] text-secondary/60">{messages.length} ENTRIES</span>
        </div>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-3 pr-2"
        style={{
          scrollbarWidth: "thin",
          scrollbarColor: "hsl(195 100% 55% / 0.3) transparent"
        }}
      >
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-8">
            <div 
              className="w-12 h-12 rounded-full mb-4 animate-pulse"
              style={{
                background: "radial-gradient(circle, hsl(195 100% 55% / 0.2) 0%, transparent 70%)"
              }}
            />
            <p className="text-muted-foreground text-[10px] tracking-wider">
              AWAITING INPUT, SIR
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={message.id}
              className={`
                animate-fade-in-up
                ${message.isUser ? "text-right" : "text-left"}
              `}
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <div
                className={`
                  inline-block max-w-[90%] px-3 py-2 rounded-lg text-xs
                  ${message.isUser 
                    ? "bg-secondary/10 text-secondary border border-secondary/20" 
                    : "bg-primary/10 text-primary border border-primary/20"
                  }
                `}
                style={{
                  boxShadow: message.isUser 
                    ? "0 0 10px hsl(210 100% 70% / 0.1)" 
                    : "0 0 10px hsl(195 100% 55% / 0.1)"
                }}
              >
                <div className={`mb-1 text-[8px] tracking-wider ${
                  message.isUser ? "text-secondary/50" : "text-primary/50"
                }`}>
                  {message.isUser ? "USER" : "J.A.R.V.I.S."}
                </div>
                {message.text}
              </div>
              <div className="text-[8px] text-muted-foreground mt-1 px-1 tracking-wider">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ResponsePanel;