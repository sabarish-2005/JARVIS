"""
==================== ACTION EXECUTOR MODULE ====================
Executes parsed commands using appropriate controllers
"""

import datetime
import subprocess
import webbrowser
import psutil
import os
from browser_control import BrowserController
from system_control import SystemController
from ai_brain import AIBrain
from rich.console import Console

console = Console()

class ActionExecutor:
    """Executes actions based on parsed intent"""
    
    def __init__(self):
        self.system = SystemController()
        self.ai = AIBrain()
        console.print("[green]⚡ Action executor initialized[/green]")
    
    def execute(self, intent):
        """
        Execute action based on intent
        
        Args:
            intent: Parsed intent dictionary
        
        Returns:
            dict: Execution result with success status and message
        """
        action = intent['action']
        params = intent.get('params', {})
        
        try:
            # Route to appropriate handler
            if action == 'play_youtube':
                return self._play_youtube(params)
            elif action == 'open_app':
                return self._open_app(params)
            elif action == 'close_app':
                return self._close_app(params)
            elif action == 'volume_up':
                return self._volume_up()
            elif action == 'volume_down':
                return self._volume_down()
            elif action == 'mute':
                return self._mute()
            elif action == 'screenshot':
                return self._screenshot()
            elif action == 'shutdown':
                return self._shutdown(params)
            elif action == 'restart':
                return self._restart()
            elif action == 'lock':
                return self._lock()
            elif action == 'search_google':
                return self._search_google(params)
            elif action == 'search_web':
                return self._search_web(params)
            elif action == 'whatsapp_message':
                return self._whatsapp_message(params)
            elif action == 'time':
                return self._tell_time()
            elif action == 'date':
                return self._tell_date()
            elif action == 'system_info':
                return self._system_info()
            elif action == 'memory_info':
                return self._memory_info()
            elif action == 'disk_info':
                return self._disk_info()
            elif action == 'battery_info':
                return self._battery_info()
            elif action == 'chat':
                return self._ai_chat(params)
            else:
                return {'success': False, 'error': 'Unknown action'}
                
        except Exception as e:
            console.print(f"[red]Execution error: {e}[/red]")
            return {'success': False, 'error': str(e)}
    
    def _play_youtube(self, params):
        """Play YouTube video - searches and opens results"""
        query = params.get('query', '')
        
        try:
            if not query:
                # Open YouTube homepage
                subprocess.run(['cmd', '/c', 'start', 'chrome', 'https://www.youtube.com'], shell=False)
                return {'success': True, 'message': 'Opening YouTube, Sir.'}
            
            # Clean up the query
            search_query = query.strip().replace(" ", "+")
            
            # YouTube search URL
            search_url = f'https://www.youtube.com/results?search_query={search_query}'
            
            # Open in Chrome
            try:
                subprocess.run(['cmd', '/c', 'start', 'chrome', search_url], shell=False)
            except Exception:
                webbrowser.open(search_url)
            
            return {'success': True, 'message': f'Searching "{query}" on YouTube, Sir.'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _open_app(self, params):
        """Open application - supports 100+ apps"""
        app = params.get('app', '').strip()
        if not app:
            return {'success': False, 'error': 'No app specified'}
        
        # Special handling for certain apps
        special_responses = {
            'youtube': 'Opening YouTube in your browser, Sir.',
            'spotify': 'Launching Spotify, Sir. Enjoy your music.',
            'settings': 'Opening system settings, Sir.',
            'calculator': 'Opening calculator, Sir.',
            'this pc': 'Opening This PC, Sir. You can view your drives and storage.',
            'my computer': 'Opening This PC, Sir.',
            'file explorer': 'Opening File Explorer, Sir.',
            'chrome': 'Launching Google Chrome, Sir.',
            'notepad': 'Opening Notepad, Sir.',
            'task manager': 'Opening Task Manager, Sir. You can monitor system performance.',
            'control panel': 'Opening Control Panel, Sir.',
            'discord': 'Opening Discord, Sir.',
            'vscode': 'Opening Visual Studio Code, Sir.',
            'terminal': 'Opening Windows Terminal, Sir.',
            'gmail': 'Opening Gmail in your browser, Sir.',
            'github': 'Opening GitHub in your browser, Sir.',
        }
        
        success = self.system.open_application(app)
        if success:
            # Get custom response or default
            response = special_responses.get(app.lower(), f'Opening {app}, Sir.')
            return {'success': True, 'message': response}
        else:
            return {'success': False, 'error': f'Could not open {app}. It may not be installed.'}
    
    def _close_app(self, params):
        """Close application"""
        app = params.get('app', '').strip()
        if not app:
            return {'success': False, 'error': 'No app specified'}
        
        success = self.system.close_application(app)
        if success:
            return {'success': True, 'message': f'Closed {app}, Sir.'}
        else:
            return {'success': False, 'error': f'{app} is not currently running, Sir.'}
    
    def _volume_up(self):
        """Increase volume"""
        success = self.system.volume_up()
        if success:
            return {'success': True, 'message': 'Volume increased, Sir.'}
        else:
            return {'success': False, 'error': 'Failed to increase volume'}
    
    def _volume_down(self):
        """Decrease volume"""
        success = self.system.volume_down()
        if success:
            return {'success': True, 'message': 'Volume decreased, Sir.'}
        else:
            return {'success': False, 'error': 'Failed to decrease volume'}
    
    def _mute(self):
        """Toggle mute"""
        success = self.system.mute()
        if success:
            return {'success': True, 'message': 'Mute toggled, Sir.'}
        else:
            return {'success': False, 'error': 'Failed to toggle mute'}
    
    def _screenshot(self):
        """Take screenshot"""
        filename = self.system.take_screenshot()
        if filename:
            return {'success': True, 'message': f'Screenshot captured and saved, Sir.'}
        else:
            return {'success': False, 'error': 'Failed to take screenshot'}
    
    def _shutdown(self, params):
        """Shutdown system"""
        minutes = params.get('minutes', 0)
        success = self.system.shutdown(minutes)
        if success:
            if minutes > 0:
                return {'success': True, 'message': f'System will shutdown in {minutes} minutes, Sir.'}
            else:
                return {'success': True, 'message': 'Initiating system shutdown, Sir. Goodbye.'}
        else:
            return {'success': False, 'error': 'Failed to schedule shutdown'}
    
    def _restart(self):
        """Restart system"""
        success = self.system.restart()
        if success:
            return {'success': True, 'message': 'Restarting system, Sir. See you in a moment.'}
        else:
            return {'success': False, 'error': 'Failed to restart'}
    
    def _lock(self):
        """Lock screen"""
        success = self.system.lock_screen()
        if success:
            return {'success': True, 'message': 'Locking your screen, Sir.'}
        else:
            return {'success': False, 'error': 'Failed to lock screen'}
    
    def _search_google(self, params):
        """Search Google"""
        query = params.get('query', '')
        if not query:
            return {'success': False, 'error': 'No search query provided'}
        
        try:
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            subprocess.run(['cmd', '/c', 'start', 'chrome', search_url], shell=False)
            return {'success': True, 'message': f'Searching Google for "{query}", Sir.'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _search_web(self, params):
        """Generic web search"""
        query = params.get('query', '')
        if not query:
            return {'success': False, 'error': 'No search query provided'}
        
        try:
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            webbrowser.open(search_url)
            return {'success': True, 'message': f'Searching for "{query}", Sir.'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _whatsapp_message(self, params):
        """Send WhatsApp message"""
        contact = params.get('contact', '')
        if not contact:
            return {'success': False, 'error': 'No contact specified'}
        
        try:
            webbrowser.open("https://web.whatsapp.com")
            return {'success': True, 'message': f'Opening WhatsApp Web, Sir. You can search for {contact}.'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _tell_time(self):
        """Tell current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return {'success': True, 'message': f'The current time is {time_str}, Sir.'}
    
    def _tell_date(self):
        """Tell current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return {'success': True, 'message': f'Today is {date_str}, Sir.'}
    
    def _system_info(self):
        """Get complete system information"""
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Battery info
            battery_str = ""
            try:
                battery = psutil.sensors_battery()
                if battery:
                    status = "charging" if battery.power_plugged else "on battery"
                    battery_str = f" Battery is at {battery.percent}% and {status}."
            except:
                pass
            
            message = (
                f"System Status, Sir: CPU usage is {cpu}%. "
                f"Memory usage is {memory.percent}% with {round(memory.available / (1024**3), 1)} GB available. "
                f"Primary disk is {disk.percent}% full with {round(disk.free / (1024**3), 1)} GB free.{battery_str}"
            )
            
            return {'success': True, 'message': message}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _memory_info(self):
        """Get memory/RAM information"""
        try:
            memory = psutil.virtual_memory()
            total_gb = round(memory.total / (1024**3), 1)
            used_gb = round(memory.used / (1024**3), 1)
            available_gb = round(memory.available / (1024**3), 1)
            
            message = (
                f"Memory Status, Sir: You have {total_gb} GB total RAM. "
                f"Currently using {used_gb} GB ({memory.percent}%). "
                f"{available_gb} GB is available."
            )
            
            return {'success': True, 'message': message}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _disk_info(self):
        """Get disk/storage information"""
        try:
            partitions = psutil.disk_partitions()
            disk_info = []
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = round(usage.total / (1024**3), 1)
                    used_gb = round(usage.used / (1024**3), 1)
                    free_gb = round(usage.free / (1024**3), 1)
                    
                    disk_info.append(
                        f"Drive {partition.device.replace(chr(92), '')}: {total_gb} GB total, "
                        f"{used_gb} GB used, {free_gb} GB free ({usage.percent}% used)"
                    )
                except:
                    continue
            
            if disk_info:
                message = "Storage Status, Sir: " + ". ".join(disk_info[:3])  # Limit to 3 drives
            else:
                disk = psutil.disk_usage('/')
                message = f"Primary disk: {disk.percent}% used with {round(disk.free / (1024**3), 1)} GB free."
            
            return {'success': True, 'message': message}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _battery_info(self):
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "charging" if battery.power_plugged else "discharging"
                
                # Calculate time remaining
                time_str = ""
                if battery.secsleft > 0 and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    if hours > 0:
                        time_str = f" Approximately {hours} hours and {minutes} minutes remaining."
                    else:
                        time_str = f" Approximately {minutes} minutes remaining."
                
                message = f"Battery is at {battery.percent}% and currently {status}.{time_str}"
            else:
                message = "No battery detected. This appears to be a desktop system, Sir."
            
            return {'success': True, 'message': message}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _ai_chat(self, params):
        """Chat with AI"""
        message = params.get('message', '')
        if not message:
            return {'success': False, 'error': 'No message provided'}
        
        response = self.ai.chat(message)
        if response:
            return {'success': True, 'message': response}
        else:
            return {'success': False, 'error': 'AI response failed'}
