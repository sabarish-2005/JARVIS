"""
==================== VOICE ENGINE MODULE ====================
Handles speech recognition and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
import threading
from rich.console import Console

console = Console()

class VoiceEngine:
    """Voice recognition and speech synthesis"""
    
    def __init__(self):
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.0
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        # Detect microphone availability early to avoid runtime crashes when none exist
        try:
            device_names = sr.Microphone.list_microphone_names()
            self.has_microphone = bool(device_names)
            if not self.has_microphone:
                console.print("[yellow]⚠️ No microphone detected on this system[/yellow]")
        except Exception as e:
            self.has_microphone = False
            console.print(f"[yellow]⚠️ Microphone detection failed: {e}[/yellow]")
        
        # Text-to-Speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 0.9)
        
        # Set voice (try to get a good one)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'david' in voice.name.lower() or 'zira' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break

        # Serialize TTS calls to avoid "run loop already started" errors
        self.tts_lock = threading.Lock()
        
        console.print("[green]🎤 Voice engine initialized[/green]")
    
    def listen(self, timeout=5):
        """
        Listen for voice input
        
        Args:
            timeout: Maximum time to wait for input
        
        Returns:
            str: Recognized text or None
        """
        try:
            if not getattr(self, 'has_microphone', True):
                return None

            with sr.Microphone() as source:
                # Adjust for ambient noise quickly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                # Listen for audio with increased sensitivity
                console.print("[dim]Listening...[/dim]", end="\r")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                return text
                
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            console.print(f"[red]Speech recognition error: {e}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Listen error: {e}[/red]")
            return None
    
    def speak(self, text):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
        """
        try:
            console.print(f"[blue]JARVIS: {text}[/blue]")
            
            # Use a lock to ensure only one runAndWait is active at a time
            with self.tts_lock:
                self.engine.stop()  # stop any residual queue
                self.engine.say(text)
                self.engine.runAndWait()
            
        except Exception as e:
            console.print(f"[red]Speak error: {e}[/red]")
    
    def test_microphone(self):
        """Test microphone functionality"""
        console.print("[yellow]Testing microphone... Say something![/yellow]")
        text = self.listen(timeout=5)
        
        if text:
            console.print(f"[green]✅ Heard: {text}[/green]")
            self.speak(f"I heard: {text}")
            return True
        else:
            console.print("[red]❌ No audio detected[/red]")
            return False
