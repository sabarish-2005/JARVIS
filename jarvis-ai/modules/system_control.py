"""
==================== SYSTEM CONTROL MODULE ====================
Windows system automation and control
"""

import pyautogui
import psutil
import subprocess
import os
import time
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from rich.console import Console

console = Console()

class SystemController:
    """Controls Windows system operations"""
    
    def __init__(self):
        # PyAutoGUI settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Audio control
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        except:
            self.volume = None
            console.print("[yellow]⚠️ Audio control not available[/yellow]")
        
        # Comprehensive app mappings
        self.app_map = {
            # System Apps
            'calculator': 'calc',
            'calc': 'calc',
            'notepad': 'notepad',
            'paint': 'mspaint',
            'task manager': 'taskmgr',
            'taskmgr': 'taskmgr',
            'snipping tool': 'snippingtool',
            'snip': 'snippingtool',
            'wordpad': 'wordpad',
            'character map': 'charmap',
            'magnifier': 'magnify',
            'narrator': 'narrator',
            'on screen keyboard': 'osk',
            'osk': 'osk',
            'disk cleanup': 'cleanmgr',
            'defragment': 'dfrgui',
            'device manager': 'devmgmt.msc',
            'disk management': 'diskmgmt.msc',
            'event viewer': 'eventvwr.msc',
            'services': 'services.msc',
            'system information': 'msinfo32',
            'resource monitor': 'resmon',
            'performance monitor': 'perfmon',
            'registry editor': 'regedit',
            'remote desktop': 'mstsc',
            
            # File Explorer variants
            'explorer': 'explorer',
            'file explorer': 'explorer',
            'files': 'explorer',
            'this pc': 'explorer ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}',
            'my computer': 'explorer ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}',
            'computer': 'explorer ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}',
            'recycle bin': 'explorer ::{645FF040-5081-101B-9F08-00AA002F954E}',
            'trash': 'explorer ::{645FF040-5081-101B-9F08-00AA002F954E}',
            'downloads': f'explorer {os.path.expanduser("~")}\\Downloads',
            'documents': f'explorer {os.path.expanduser("~")}\\Documents',
            'desktop': f'explorer {os.path.expanduser("~")}\\Desktop',
            'pictures': f'explorer {os.path.expanduser("~")}\\Pictures',
            'videos': f'explorer {os.path.expanduser("~")}\\Videos',
            'music': f'explorer {os.path.expanduser("~")}\\Music',
            
            # Settings & Control Panel
            'settings': 'start ms-settings:',
            'setting': 'start ms-settings:',
            'control panel': 'control',
            'control': 'control',
            'bluetooth': 'start ms-settings:bluetooth',
            'wifi': 'start ms-settings:network-wifi',
            'wifi settings': 'start ms-settings:network-wifi',
            'network': 'start ms-settings:network',
            'display': 'start ms-settings:display',
            'display settings': 'start ms-settings:display',
            'sound settings': 'start ms-settings:sound',
            'battery': 'start ms-settings:batterysaver',
            'battery settings': 'start ms-settings:batterysaver',
            'power': 'start ms-settings:powersleep',
            'power settings': 'start ms-settings:powersleep',
            'storage': 'start ms-settings:storagesense',
            'storage settings': 'start ms-settings:storagesense',
            'apps': 'start ms-settings:appsfeatures',
            'apps settings': 'start ms-settings:appsfeatures',
            'personalization': 'start ms-settings:personalization',
            'wallpaper': 'start ms-settings:personalization-background',
            'themes': 'start ms-settings:themes',
            'lock screen': 'start ms-settings:lockscreen',
            'privacy': 'start ms-settings:privacy',
            'update': 'start ms-settings:windowsupdate',
            'windows update': 'start ms-settings:windowsupdate',
            'about': 'start ms-settings:about',
            'system info': 'start ms-settings:about',
            'date time': 'start ms-settings:dateandtime',
            'time settings': 'start ms-settings:dateandtime',
            'language': 'start ms-settings:regionlanguage',
            'keyboard settings': 'start ms-settings:keyboard',
            'mouse settings': 'start ms-settings:mousetouchpad',
            'notifications': 'start ms-settings:notifications',
            'focus assist': 'start ms-settings:quiethours',
            'gaming': 'start ms-settings:gaming-gamebar',
            'game bar': 'start ms-settings:gaming-gamebar',
            'camera settings': 'start ms-settings:privacy-webcam',
            'microphone settings': 'start ms-settings:privacy-microphone',
            
            # Browsers
            'chrome': 'start chrome',
            'google chrome': 'start chrome',
            'google': 'start chrome',
            'edge': 'start msedge',
            'microsoft edge': 'start msedge',
            'firefox': 'start firefox',
            'brave': 'start brave',
            'opera': 'start opera',
            
            # Microsoft Office
            'word': 'start winword',
            'microsoft word': 'start winword',
            'excel': 'start excel',
            'microsoft excel': 'start excel',
            'powerpoint': 'start powerpnt',
            'ppt': 'start powerpnt',
            'outlook': 'start outlook',
            'onenote': 'start onenote',
            'access': 'start msaccess',
            'teams': 'start msteams:',
            'microsoft teams': 'start msteams:',
            
            # Development Tools
            'vscode': 'code',
            'vs code': 'code',
            'visual studio code': 'code',
            'visual studio': 'start devenv',
            'cmd': 'start cmd',
            'command prompt': 'start cmd',
            'terminal': 'start wt',
            'windows terminal': 'start wt',
            'powershell': 'start powershell',
            'git bash': 'start "C:\\Program Files\\Git\\git-bash.exe"',
            'postman': 'start postman',
            'docker': 'start docker',
            
            # Media & Entertainment
            'spotify': 'start spotify:',
            'vlc': 'start vlc',
            'media player': 'start wmplayer',
            'windows media player': 'start wmplayer',
            'movies': 'start mswindowsvideo:',
            'movies and tv': 'start mswindowsvideo:',
            'groove music': 'start mswindowsmusic:',
            'photos': 'start ms-photos:',
            'camera': 'start microsoft.windows.camera:',
            'voice recorder': 'start soundrecorder:',
            'xbox': 'start xbox:',
            'xbox game bar': 'start ms-gamebar:',
            
            # Communication
            'skype': 'start skype:',
            'zoom': 'start zoommtg:',
            'discord': 'start discord:',
            'slack': 'start slack:',
            'telegram': 'start telegram:',
            'whatsapp': 'start whatsapp:',
            
            # Utilities
            'calendar': 'start outlookcal:',
            'mail': 'start outlookmail:',
            'weather': 'start bingweather:',
            'maps': 'start bingmaps:',
            'news': 'start bingnews:',
            'clock': 'start ms-clock:',
            'alarms': 'start ms-clock:',
            'store': 'start ms-windows-store:',
            'microsoft store': 'start ms-windows-store:',
            'sticky notes': 'start ms-stickynotes:',
            'screen recording': 'start ms-screenclip:',
            
            # Gaming
            'steam': 'start steam:',
            'epic games': 'start com.epicgames.launcher:',
            
            # Social Media URLs
            'youtube': 'start chrome https://www.youtube.com',
            'facebook': 'start chrome https://www.facebook.com',
            'instagram': 'start chrome https://www.instagram.com',
            'twitter': 'start chrome https://www.twitter.com',
            'x': 'start chrome https://www.x.com',
            'linkedin': 'start chrome https://www.linkedin.com',
            'reddit': 'start chrome https://www.reddit.com',
            'github': 'start chrome https://www.github.com',
            'gmail': 'start chrome https://mail.google.com',
            'google drive': 'start chrome https://drive.google.com',
            'google docs': 'start chrome https://docs.google.com',
            'google sheets': 'start chrome https://sheets.google.com',
            'netflix': 'start chrome https://www.netflix.com',
            'amazon': 'start chrome https://www.amazon.com',
            'flipkart': 'start chrome https://www.flipkart.com',
            'chatgpt': 'start chrome https://chat.openai.com',
            'claude': 'start chrome https://claude.ai',
        }
        
        # Process name mappings for closing apps
        self.process_map = {
            'chrome': 'chrome.exe',
            'google chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'microsoft edge': 'msedge.exe',
            'firefox': 'firefox.exe',
            'notepad': 'notepad.exe',
            'calculator': 'Calculator.exe',
            'calc': 'Calculator.exe',
            'spotify': 'Spotify.exe',
            'vscode': 'Code.exe',
            'vs code': 'Code.exe',
            'word': 'WINWORD.EXE',
            'excel': 'EXCEL.EXE',
            'powerpoint': 'POWERPNT.EXE',
            'outlook': 'OUTLOOK.EXE',
            'teams': 'Teams.exe',
            'discord': 'Discord.exe',
            'slack': 'slack.exe',
            'zoom': 'Zoom.exe',
            'vlc': 'vlc.exe',
            'steam': 'steam.exe',
            'explorer': 'explorer.exe',
            'task manager': 'Taskmgr.exe',
            'paint': 'mspaint.exe',
            'settings': 'SystemSettings.exe',
        }
        
        console.print("[green]🖥️ System controller initialized[/green]")
    
    def open_application(self, app_name):
        """
        Open application by name
        
        Args:
            app_name: Application name or path
        """
        try:
            app_lower = app_name.lower().strip()
            
            # Check if app is in our mapping
            if app_lower in self.app_map:
                command = self.app_map[app_lower]
            else:
                # Try to open as-is
                command = f'start {app_name}'
            
            subprocess.Popen(command, shell=True)
            console.print(f"[green]✅ Opened {app_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Failed to open {app_name}: {e}[/red]")
            return False
    
    def close_application(self, app_name):
        """Close application by name"""
        try:
            app_lower = app_name.lower().strip()
            
            # Get process name from mapping
            process_name = self.process_map.get(app_lower, f'{app_name}.exe')
            
            closed = False
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    proc_name = proc.info['name'].lower()
                    if app_lower in proc_name or process_name.lower() == proc_name:
                        proc.kill()
                        closed = True
                        console.print(f"[green]✅ Closed {proc.info['name']}[/green]")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                return True
            
            console.print(f"[yellow]{app_name} not running[/yellow]")
            return False
            
        except Exception as e:
            console.print(f"[red]Failed to close {app_name}: {e}[/red]")
            return False
    
    def volume_up(self, amount=10):
        """Increase system volume"""
        try:
            if self.volume:
                current = self.volume.GetMasterVolumeLevelScalar()
                new_volume = min(1.0, current + (amount / 100))
                self.volume.SetMasterVolumeLevelScalar(new_volume, None)
                console.print(f"[green]✅ Volume: {int(new_volume * 100)}%[/green]")
                return True
            else:
                # Fallback: use keyboard
                for _ in range(amount // 2):
                    pyautogui.press('volumeup')
                return True
        except Exception as e:
            console.print(f"[red]Volume error: {e}[/red]")
            return False
    
    def volume_down(self, amount=10):
        """Decrease system volume"""
        try:
            if self.volume:
                current = self.volume.GetMasterVolumeLevelScalar()
                new_volume = max(0.0, current - (amount / 100))
                self.volume.SetMasterVolumeLevelScalar(new_volume, None)
                console.print(f"[green]✅ Volume: {int(new_volume * 100)}%[/green]")
                return True
            else:
                # Fallback: use keyboard
                for _ in range(amount // 2):
                    pyautogui.press('volumedown')
                return True
        except Exception as e:
            console.print(f"[red]Volume error: {e}[/red]")
            return False
    
    def mute(self):
        """Toggle mute"""
        try:
            if self.volume:
                self.volume.SetMute(not self.volume.GetMute(), None)
                console.print("[green]✅ Mute toggled[/green]")
                return True
            else:
                pyautogui.press('volumemute')
                return True
        except Exception as e:
            console.print(f"[red]Mute error: {e}[/red]")
            return False
    
    def take_screenshot(self, filename=None):
        """Take screenshot"""
        try:
            if not filename:
                filename = f"screenshot_{int(time.time())}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            console.print(f"[green]✅ Screenshot saved: {filename}[/green]")
            return filename
        except Exception as e:
            console.print(f"[red]Screenshot error: {e}[/red]")
            return None
    
    def shutdown(self, minutes=0):
        """Shutdown system"""
        try:
            seconds = minutes * 60
            subprocess.run(f'shutdown /s /t {seconds}', shell=True)
            console.print(f"[green]✅ Shutdown scheduled in {minutes} minutes[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Shutdown error: {e}[/red]")
            return False
    
    def restart(self, minutes=0):
        """Restart system"""
        try:
            seconds = minutes * 60
            subprocess.run(f'shutdown /r /t {seconds}', shell=True)
            console.print(f"[green]✅ Restart scheduled in {minutes} minutes[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Restart error: {e}[/red]")
            return False
    
    def lock_screen(self):
        """Lock Windows screen"""
        try:
            subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
            console.print("[green]✅ Screen locked[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Lock error: {e}[/red]")
            return False
    
    def type_text(self, text):
        """Type text using keyboard automation"""
        try:
            pyautogui.write(text, interval=0.05)
            console.print(f"[green]✅ Typed: {text}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Type error: {e}[/red]")
            return False
    
    def press_key(self, key):
        """Press specific key"""
        try:
            pyautogui.press(key)
            console.print(f"[green]✅ Pressed: {key}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Key press error: {e}[/red]")
            return False
    
    def get_system_info(self):
        """Get system information"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            info = {
                'cpu': cpu,
                'memory': memory,
                'disk': disk
            }
            
            console.print(f"[cyan]CPU: {cpu}% | RAM: {memory}% | Disk: {disk}%[/cyan]")
            return info
        except Exception as e:
            console.print(f"[red]System info error: {e}[/red]")
            return None
