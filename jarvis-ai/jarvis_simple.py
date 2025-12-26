# Import JARVIS modules
from modules.ai_brain import AIBrain
import speech_recognition as sr
import pyttsx3
import pyautogui
import pyperclip

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except:
            return ""

def open_app(name):
    """Open applications and websites"""
    name = name.lower().strip()
    
    # Website shortcuts
    websites = {
        'gmail': 'https://gmail.com',
        'youtube': 'https://youtube.com',
        'google': 'https://google.com',
        'facebook': 'https://facebook.com',
        'twitter': 'https://twitter.com',
        'instagram': 'https://instagram.com'
    }
    
    # Special folders and common apps
    folders = {
        'videos': 'explorer.exe shell:MyVideosFolder',
        'video': 'explorer.exe shell:MyVideosFolder', 
        'documents': 'explorer.exe shell:MyDocumentsFolder',
        'document': 'explorer.exe shell:MyDocumentsFolder',
        'downloads': 'explorer.exe shell:DownloadsFolder',
        'download': 'explorer.exe shell:DownloadsFolder',
        'pictures': 'explorer.exe shell:MyPicturesFolder',
        'picture': 'explorer.exe shell:MyPicturesFolder',
        'music': 'explorer.exe shell:MyMusicFolder',
        'desktop': 'explorer.exe shell:DesktopFolder',
        'c drive': 'explorer.exe C:\\',
        'd drive': 'explorer.exe D:\\'
    }
    
    # Application shortcuts
    apps = {
        'chrome': ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', 'start chrome'],
        'firefox': ['C:\\Program Files\\Mozilla Firefox\\firefox.exe', 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', 'start firefox'],
        'edge': 'start msedge',
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'word': ['C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE', 'start winword'],
        'excel': ['C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE', 'start excel'],
        'powerpoint': ['C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE', 'start powerpnt'],
        'file explorer': 'explorer.exe',
        'explorer': 'explorer.exe',
        'file manager': 'explorer.exe',
        'settings': 'start ms-settings:',
        'control panel': 'control.exe',
        'task manager': 'taskmgr.exe',
        'cmd': 'cmd.exe',
        'command prompt': 'cmd.exe',
        'powershell': 'powershell.exe'
    }
    
    try:
        if name in websites:
            # Open website
            webbrowser.open(websites[name])
            return f"Opening {name}"
        elif name in folders:
            # Open special folder
            cmd = folders[name]
            print(f"Opening folder {name} with: {cmd}")
            subprocess.Popen(cmd, shell=True)
            print(f"Successfully opened {name} folder")
            return f"Opening {name} folder"
        elif name in apps:
            # Open application
            app_paths = apps[name]
            if isinstance(app_paths, list):
                # Try each path until one works
                for path in app_paths:
                    try:
                        print(f"Trying to open {name} with: {path}")
                        if path.startswith('start '):
                            subprocess.Popen(path, shell=True)
                        else:
                            subprocess.Popen(path)
                        print(f"Successfully opened {name}")
                        return f"Opening {name}"
                    except Exception as e:
                        print(f"Failed to open {name} with {path}: {e}")
                        continue
                # If none worked, show error
                print(f"Could not open {name} - all paths failed")
                return f"Could not open {name}"
            else:
                # Single path/command
                cmd = app_paths
                try:
                    print(f"Opening {name} with: {cmd}")
                    if cmd.startswith('start '):
                        subprocess.Popen(cmd, shell=True)
                    else:
                        subprocess.Popen(cmd)
                    print(f"Successfully opened {name}")
                    return f"Opening {name}"
                except Exception as e:
                    print(f"Failed to open {name}: {e}")
                    return f"Could not open {name}"
        else:
            # Try to open as general command
            try:
                print(f"Trying to open unknown app/folder: {name}")
                subprocess.Popen(f'start {name}', shell=True)
                print(f"Successfully opened {name} with start command")
                return f"Opening {name}"
            except Exception as e:
                print(f"Failed to open {name}: {e}")
                return f"Could not open {name} - app not found"
    except Exception as e:
        print(f"Error opening {name}: {e}")
        return f"Could not open {name}"

def mouse_control(action):
    """Control mouse input"""
    try:
        if action == 'click' or action == 'left click':
            pyautogui.click()
            return "Clicked"
        elif action == 'right click':
            pyautogui.rightClick()
            return "Right clicked"
        elif action == 'double click':
            pyautogui.doubleClick()
            return "Double clicked"
        elif action == 'scroll up':
            pyautogui.scroll(5)
            return "Scrolled up"
        elif action == 'scroll down':
            pyautogui.scroll(-5)
            return "Scrolled down"
        elif action.startswith('move ') or 'move to' in action:
            # Parse coordinates like "move to 100 200"
            try:
                coords = action.replace('move to ', '').replace('move ', '').strip()
                x, y = map(int, coords.split())
                pyautogui.moveTo(x, y)
                return f"Moved cursor to {x}, {y}"
            except:
                pass
            return "Could not parse coordinates"
        else:
            return f"Unknown mouse action: {action}"
    except Exception as e:
        print(f"Mouse control error: {e}")
        return f"Could not perform mouse action: {action}"

def keyboard_control(action):
    """Control keyboard input"""
    try:
        if action.startswith('type ') or action.startswith('write '):
            text = action.replace('type ', '').replace('write ', '').strip()
            pyautogui.write(text)
            return f"Typed: {text}"
        elif action == 'enter':
            pyautogui.press('enter')
            return "Pressed Enter"
        elif action == 'space':
            pyautogui.press('space')
            return "Pressed Space"
        elif action == 'backspace':
            pyautogui.press('backspace')
            return "Pressed Backspace"
        elif action == 'tab':
            pyautogui.press('tab')
            return "Pressed Tab"
        elif action.startswith('press '):
            key = action.replace('press ', '').strip()
            pyautogui.press(key)
            return f"Pressed {key}"
        else:
            return f"Unknown keyboard action: {action}"
    except Exception as e:
        print(f"Keyboard control error: {e}")
        return f"Could not perform keyboard action: {action}"

def close_app(name):
    """Close applications"""
    name = name.lower().strip()
    
    # Application process names to kill
    close_commands = {
        'chrome': 'chrome.exe',
        'firefox': 'firefox.exe', 
        'edge': 'msedge.exe',
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe',
        'powerpoint': 'powerpnt.exe',
        'explorer': 'explorer.exe',
        'file explorer': 'explorer.exe',
        'task manager': 'taskmgr.exe',
        'settings': 'SystemSettings.exe',
        'control panel': 'control.exe',
        'command prompt': 'cmd.exe',
        'powershell': 'powershell.exe',
        'taskmgr': 'taskmgr.exe'
    }
    
    try:
        if name in close_commands:
            # Kill the process
            subprocess.run(['taskkill', '/F', '/IM', close_commands[name]], 
                         capture_output=True, check=False)
            return f"Closing {name}"
        else:
            # Try alternative methods
            # Try to close by window title using taskkill
            try:
                subprocess.run(['taskkill', '/F', '/FI', f'WINDOWTITLE eq {name}*'], 
                             capture_output=True, check=False)
                return f"Closing {name}"
            except:
                pass
            
            # Try to close using WMIC (Windows Management Instrumentation)
            try:
                subprocess.run(['wmic', 'process', 'where', f'name like "%{name}%"', 'delete'], 
                             capture_output=True, check=False)
                return f"Closing {name}"
            except:
                pass
            
            return f"Could not find {name} to close"
    except Exception as e:
        print(f"Error closing {name}: {e}")
        return f"Could not close {name}"

def main():
    speak("JARVIS ready Sir")
    last_command = ""
    last_command_time = 0
    
    # Initialize AI Brain for chat functionality
    ai = AIBrain()
    
    while True:
        text = listen()
        if text:
            # Check if this is a direct command or contains wake word
            if 'jarvis' in text:
                # Remove jarvis from the command
                command = text.replace('jarvis', '').strip()
                
                # If command is empty, ask for command
                if not command:
                    speak("Yes Sir?")
                    command = listen()
                
                if command:
                    # Prevent duplicate commands (same command within 2 seconds)
                    current_time = time.time()
                    if command == last_command and current_time - last_command_time < 2:
                        print(f"Duplicate command ignored: {command}")
                        continue
                    
                    last_command = command
                    last_command_time = current_time
                    
                    print(f"Processing command: {command}")
                    
                    if 'youtube' in command:
                        if 'play' in command and ('video' in command or 'song' in command or 'music' in command):
                            # Handle "play [video/song/music] on/in youtube"
                            query = command.replace('play', '').replace('video', '').replace('song', '').replace('music', '').replace('on youtube', '').replace('in youtube', '').replace('youtube', '').strip()
                            if query:
                                webbrowser.open(f'https://youtube.com/results?search_query={query}')
                                speak(f"Searching for {query} on YouTube")
                            else:
                                speak("What would you like to play on YouTube?")
                        elif 'play' in command or 'pause' in command:
                            result = control_youtube('play')
                            speak(result)
                        elif 'next' in command:
                            result = control_youtube('next')
                            speak(result)
                        elif 'previous' in command or 'back' in command:
                            result = control_youtube('previous')
                            speak(result)
                        elif 'fullscreen' in command:
                            result = control_youtube('fullscreen')
                            speak(result)
                        elif 'mute' in command:
                            result = control_youtube('mute')
                            speak(result)
                        elif 'open' in command or 'go to' in command:
                            webbrowser.open('https://youtube.com')
                            speak("Opening YouTube")
                        else:
                            webbrowser.open('https://youtube.com')
                            speak("Opening YouTube")
                    elif command.startswith('open '):
                        app = command.replace('open', '').strip()
                        if app:
                            result = open_app(app)
                            speak(result)
                        else:
                            speak("What would you like me to open?")
                    elif command.startswith('close ') or command.startswith('kill '):
                        app = command.replace('close', '').replace('kill', '').strip()
                        if app:
                            result = close_app(app)
                            speak(result)
                        else:
                            speak("What would you like me to close?")
                    elif 'click' in command:
                        if 'left' in command:
                            result = mouse_control('left click')
                            speak(result)
                        elif 'right' in command:
                            result = mouse_control('right click')
                            speak(result)
                        elif 'double' in command:
                            result = mouse_control('double click')
                            speak(result)
                        else:
                            result = mouse_control('click')
                            speak(result)
                    elif 'scroll' in command:
                        if 'up' in command:
                            result = mouse_control('scroll up')
                            speak(result)
                        elif 'down' in command:
                            result = mouse_control('scroll down')
                            speak(result)
                        else:
                            speak("Scroll up or down?")
                    elif command.startswith('move ') or 'move to' in command:
                        result = mouse_control(command)
                        speak(result)
                    elif command.startswith('type ') or command.startswith('write '):
                        result = keyboard_control(command)
                        speak(result)
                    elif 'press' in command and ('enter' in command or 'space' in command or 'tab' in command or 'backspace' in command):
                        key = command.replace('press ', '').strip()
                        result = keyboard_control(f'press {key}')
                        speak(result)
                    elif 'time' in command:
                        current_time = datetime.datetime.now().strftime("%I:%M %p")
                        speak(f"Time is {current_time}")
                    elif 'stop' in command or 'exit' in command or 'quit' in command:
                        speak("Goodbye Sir")
                        break
                    elif command.startswith('chat ') or command.startswith('talk ') or command.startswith('ask '):
                        # Explicit chat command
                        chat_message = command.replace('chat ', '').replace('talk ', '').replace('ask ', '').strip()
                        if chat_message:
                            ai_response = ai.chat(chat_message)
                            speak(ai_response)
                        else:
                            speak("What would you like to chat about, Sir?")
                    else:
                        # Use AI chat for unrecognized commands
                        ai_response = ai.chat(command)
                        speak(ai_response)
            else:
                # Direct command without jarvis - process it anyway
                command = text.strip()
                if command:
                    print(f"Processing direct command: {command}")
                    
                    # Apply same duplicate prevention
                    current_time = time.time()
                    if command == last_command and current_time - last_command_time < 2:
                        print(f"Duplicate command ignored: {command}")
                        continue
                    
                    last_command = command
                    last_command_time = current_time
                    
                    # Process the same way as jarvis commands
                    if 'youtube' in command:
                        if 'play' in command and ('video' in command or 'song' in command):
                            query = command.replace('play', '').replace('on youtube', '').replace('youtube', '').replace('video', '').replace('song', '').strip()
                            if query:
                                webbrowser.open(f'https://youtube.com/results?search_query={query}')
                                speak(f"Searching for {query} on YouTube")
                            else:
                                speak("What would you like to play on YouTube?")
                        elif 'play' in command or 'pause' in command:
                            result = control_youtube('play')
                            speak(result)
                        elif 'next' in command:
                            result = control_youtube('next')
                            speak(result)
                        elif 'previous' in command or 'back' in command:
                            result = control_youtube('previous')
                            speak(result)
                        elif 'fullscreen' in command:
                            result = control_youtube('fullscreen')
                            speak(result)
                        elif 'mute' in command:
                            result = control_youtube('mute')
                            speak(result)
                        elif 'open' in command or 'go to' in command:
                            webbrowser.open('https://youtube.com')
                            speak("Opening YouTube")
                        else:
                            webbrowser.open('https://youtube.com')
                            speak("Opening YouTube")
                    elif command.startswith('open '):
                        app = command.replace('open', '').strip()
                        if app:
                            result = open_app(app)
                            speak(result)
                        else:
                            speak("What would you like me to open?")
                    elif command.startswith('close ') or command.startswith('kill '):
                        app = command.replace('close', '').replace('kill', '').strip()
                        if app:
                            result = close_app(app)
                            speak(result)
                        else:
                            speak("What would you like me to close?")
                    elif 'click' in command:
                        if 'left' in command:
                            result = mouse_control('left click')
                            speak(result)
                        elif 'right' in command:
                            result = mouse_control('right click')
                            speak(result)
                        elif 'double' in command:
                            result = mouse_control('double click')
                            speak(result)
                        else:
                            result = mouse_control('click')
                            speak(result)
                    elif 'scroll' in command:
                        if 'up' in command:
                            result = mouse_control('scroll up')
                            speak(result)
                        elif 'down' in command:
                            result = mouse_control('scroll down')
                            speak(result)
                        else:
                            speak("Scroll up or down?")
                    elif command.startswith('move ') or 'move to' in command:
                        result = mouse_control(command)
                        speak(result)
                    elif command.startswith('type ') or command.startswith('write '):
                        result = keyboard_control(command)
                        speak(result)
                    elif 'press' in command and ('enter' in command or 'space' in command or 'tab' in command or 'backspace' in command):
                        key = command.replace('press ', '').strip()
                        result = keyboard_control(f'press {key}')
                        speak(result)
                    elif 'time' in command:
                        current_time = datetime.datetime.now().strftime("%I:%M %p")
                        speak(f"Time is {current_time}")
                    elif 'stop' in command or 'exit' in command or 'quit' in command:
                        speak("Goodbye Sir")
                        break
                    elif command.startswith('chat ') or command.startswith('talk ') or command.startswith('ask '):
                        # Explicit chat command
                        chat_message = command.replace('chat ', '').replace('talk ', '').replace('ask ', '').strip()
                        if chat_message:
                            ai_response = ai.chat(chat_message)
                            speak(ai_response)
                        else:
                            speak("What would you like to chat about, Sir?")
                    else:
                        # Use AI chat for unrecognized direct commands
                        ai_response = ai.chat(command)
                        speak(ai_response)

if __name__ == "__main__":
    main()
