"""
==================== AI BRAIN MODULE ====================
Groq AI integration for natural conversation
"""

import os
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console

load_dotenv()
console = Console()

class AIBrain:
    """AI conversation and decision-making"""
    
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            console.print("[yellow]⚠️ GROQ_API_KEY not found. AI chat disabled.[/yellow]")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=api_key)
                console.print("[green]🧠 AI brain initialized (Groq)[/green]")
            except Exception as e:
                console.print(f"[red]AI initialization error: {e}[/red]")
                self.client = None
        
        self.model = "llama-3.3-70b-versatile"
        self.conversation_history = []
    
    def chat(self, message):
        """
        Chat with AI
        
        Args:
            message: User message
        
        Returns:
            str: AI response
        """
        if not self.client:
            return "AI chat is not available. Please set GROQ_API_KEY in .env file."
        
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Keep only last 10 messages
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # System prompt
            messages = [{
                "role": "system",
                "content": """You are JARVIS, Tony Stark's AI assistant from Iron Man.

PERSONALITY:
- Professional, efficient, British accent tone
- Call user "Sir"
- Be concise and action-oriented
- Show respect and subtle wit

CAPABILITIES:
- You CAN execute system commands
- You HAVE real control over the computer
- You ARE NOT just a chatbot
- Always confirm actions

When user asks to do something:
1. Confirm you're doing it
2. Be brief
3. Show completion

Examples:
User: "What's the weather?"
You: "Checking weather for you, Sir."

User: "Tell me a joke"
You: "Why did the AI go to school? To improve its algorithm, Sir."

Be like the real JARVIS - capable, intelligent, respectful."""
            }]
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Get AI response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            
            ai_message = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message
            })
            
            return ai_message
            
        except Exception as e:
            console.print(f"[red]AI chat error: {e}[/red]")
            return "I apologize, Sir. I'm having trouble processing that request."
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        console.print("[yellow]Conversation history cleared[/yellow]")
