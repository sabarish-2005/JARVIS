"""
==================== JARVIS TEST SCRIPT ====================
Test individual components
"""

import sys
from pathlib import Path

# Ensure project modules are importable
ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "modules"
if str(MODULES_DIR) not in sys.path:
    sys.path.insert(0, str(MODULES_DIR))

from rich.console import Console
from rich.panel import Panel

console = Console()

def test_voice_engine():
    """Test voice recognition and TTS"""
    console.print(Panel("[cyan]Testing Voice Engine[/cyan]"))
    
    try:
        from voice_engine import VoiceEngine
        
        voice = VoiceEngine()
        
        # Test TTS
        console.print("\n[yellow]Testing Text-to-Speech...[/yellow]")
        voice.speak("Voice engine test successful, Sir.")
        
        # Test microphone
        console.print("\n[yellow]Testing Microphone (5 seconds)...[/yellow]")
        if voice.test_microphone():
            console.print("[green]✅ Voice engine working![/green]")
            return True
        else:
            console.print("[red]❌ Microphone test failed[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ Voice engine error: {e}[/red]")
        return False

def test_system_control():
    """Test system control"""
    console.print(Panel("[cyan]Testing System Control[/cyan]"))
    
    try:
        from system_control import SystemController
        
        system = SystemController()
        
        # Test system info
        console.print("\n[yellow]Getting system info...[/yellow]")
        info = system.get_system_info()
        if info:
            console.print("[green]✅ System control working![/green]")
            return True
        else:
            console.print("[red]❌ System control failed[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ System control error: {e}[/red]")
        return False

def test_browser_control():
    """Test browser automation"""
    console.print(Panel("[cyan]Testing Browser Control[/cyan]"))
    
    try:
        from browser_control import BrowserController
        
        console.print("\n[yellow]Opening browser...[/yellow]")
        
        with BrowserController() as browser:
            success = browser.goto("https://www.google.com")
            if success:
                console.print("[green]✅ Browser control working![/green]")
                return True
            else:
                console.print("[red]❌ Browser navigation failed[/red]")
                return False
            
    except Exception as e:
        console.print(f"[red]❌ Browser control error: {e}[/red]")
        return False

def test_ai_brain():
    """Test AI integration"""
    console.print(Panel("[cyan]Testing AI Brain[/cyan]"))
    
    try:
        from ai_brain import AIBrain
        
        ai = AIBrain()
        
        console.print("\n[yellow]Testing AI chat...[/yellow]")
        response = ai.chat("Hello JARVIS")
        
        if response:
            console.print(f"[green]AI Response: {response}[/green]")
            console.print("[green]✅ AI brain working![/green]")
            return True
        else:
            console.print("[red]❌ No AI response[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ AI brain error: {e}[/red]")
        return False

def main():
    console.print(Panel.fit(
        "[bold cyan]JARVIS COMPONENT TESTS[/bold cyan]",
        border_style="cyan"
    ))
    
    tests = [
        ("Voice Engine", test_voice_engine),
        ("System Control", test_system_control),
        ("Browser Control", test_browser_control),
        ("AI Brain", test_ai_brain),
    ]
    
    results = []
    
    for name, test_func in tests:
        console.print(f"\n[bold]Running {name} test...[/bold]")
        result = test_func()
        results.append((name, result))
        console.print("")
    
    # Summary
    console.print(Panel.fit("[bold]TEST SUMMARY[/bold]", border_style="cyan"))
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[green]✅ PASS[/green]" if result else "[red]❌ FAIL[/red]"
        console.print(f"{name}: {status}")
    
    console.print(f"\n[bold]Total: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("\n[green]🎉 All tests passed! JARVIS is ready![/green]")
    else:
        console.print("\n[yellow]⚠️ Some tests failed. Check errors above.[/yellow]")

if __name__ == "__main__":
    main()
