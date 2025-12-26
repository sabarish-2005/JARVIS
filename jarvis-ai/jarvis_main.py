"""
==================== JARVIS MAIN ENTRY POINT ====================
Production-Ready Voice Assistant with Real Automation
"""

import sys
import os
import threading
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)
console = Console()

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))

# Import JARVIS modules
from voice_engine import VoiceEngine
from intent_parser import IntentParser
from action_executor import ActionExecutor
from ai_brain import AIBrain

class JARVISCore:
    """Main JARVIS AI System"""
    
    def __init__(self):
        console.print(Panel.fit(
            "[bold cyan]⚡ JARVIS AI SYSTEM INITIALIZING...[/bold cyan]",
            border_style="cyan"
        ))
        
        self.voice = VoiceEngine()
        self.parser = IntentParser()
        self.executor = ActionExecutor()
        self.ai = AIBrain()
        
        self.running = False
        self.wake_word = "jarvis"
        
        console.print("[green]✅ All systems online[/green]")
        console.print(f"[yellow]🎤 Wake word: {self.wake_word.upper()}[/yellow]")
        console.print("[cyan]🚀 Ready for commands, Sir.[/cyan]\n")
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        while self.running:
            try:
                text = self.voice.listen(timeout=5)
                if text and self.wake_word in text.lower():
                    console.print(f"\n[bold green]>>> JARVIS ACTIVATED[/bold green]")
                    self.voice.speak("Yes, Sir?")
                    self.handle_command()
            except Exception as e:
                console.print(f"[red]Listen error: {e}[/red]")
                time.sleep(1)
    
    def handle_command(self):
        """Process voice command"""
        try:
            # Give user time to speak command
            console.print("[bold cyan]🎤 Listening for command...[/bold cyan]")
            time.sleep(0.5)  # Small delay for user to prepare
            
            # Listen for actual command with longer timeout
            command = self.voice.listen(timeout=15)
            
            if not command:
                self.voice.speak("I didn't catch that, Sir.")
                return
            
            console.print(f"[cyan]Command: {command}[/cyan]")
            
            # Parse intent
            intent = self.parser.parse(command)
            console.print(f"[yellow]Intent: {intent['action']}[/yellow]")
            
            # Execute action
            result = self.executor.execute(intent)
            
            if result['success']:
                response = result.get('message', 'Done, Sir.')
                console.print(f"[green]✅ {response}[/green]")
                self.voice.speak(response)
            else:
                error_msg = result.get('error', 'Failed to execute command')
                console.print(f"[red]❌ {error_msg}[/red]")
                self.voice.speak(f"Sorry Sir, {error_msg}")
                
        except KeyboardInterrupt:
            raise
        except Exception as e:
            console.print(f"[red]Command error: {e}[/red]")
            self.voice.speak("Something went wrong, Sir.")
    
    def start(self):
        """Start JARVIS system"""
        self.running = True
        
        try:
            console.print("\n[bold]JARVIS is now listening...[/bold]")
            console.print("[dim]Say 'JARVIS' followed by your command[/dim]\n")
            
            # Start listening loop
            self.listen_for_wake_word()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down JARVIS...[/yellow]")
            self.stop()
    
    def stop(self):
        """Stop JARVIS system"""
        self.running = False
        self.voice.speak("Goodbye, Sir.")
        console.print("[green]✅ JARVIS offline[/green]")
        sys.exit(0)


def main():
    """Main entry point"""
    try:
        jarvis = JARVISCore()
        jarvis.start()
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
