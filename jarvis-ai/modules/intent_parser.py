"""
==================== INTENT PARSER MODULE ====================
Understands user commands and extracts intent
"""

import re
from rich.console import Console

console = Console()

class IntentParser:
    """Parses user commands to understand intent"""
    
    def __init__(self):
        # Comprehensive app list for pattern matching
        self.app_list = (
            'chrome|google chrome|edge|firefox|brave|opera|'
            'calculator|calc|notepad|paint|word|excel|powerpoint|outlook|'
            'powershell|cmd|terminal|command prompt|'
            'task manager|spotify|vscode|vs code|visual studio|'
            'explorer|file explorer|files|this pc|my computer|computer|'
            'downloads|documents|desktop|pictures|videos|music|'
            'settings|control panel|bluetooth|wifi|network|display|sound settings|'
            'battery|power|storage|apps|personalization|wallpaper|themes|'
            'update|windows update|about|system info|'
            'discord|slack|zoom|teams|skype|telegram|whatsapp|'
            'steam|epic games|'
            'youtube|facebook|instagram|twitter|linkedin|reddit|github|'
            'gmail|google drive|netflix|amazon|chatgpt|claude|'
            'camera|photos|calendar|mail|weather|maps|news|clock|alarms|'
            'store|microsoft store|sticky notes|'
            'vlc|media player|movies|groove music|voice recorder|xbox|'
            'recycle bin|trash'
        )
        
        # Command patterns (order matters - more specific first!)
        self.patterns = {
            'play_youtube': [
                r'(?:play|search|find)\s+(.+?)\s+(?:on\s+)?(?:youtube|video|song)',
                r'youtube\s+(?:play|search|open)?\s*(.+)?',
                r'play\s+(.+)',  # Simple "play [song name]"
                r'(.+?)\s+(?:video|song)\s+(?:play|போடு)',
            ],
            'search_google': [
                r'(?:search|google)\s+(?:for\s+)?(.+?)(?:\s+(?:in|on)\s+(?:chrome|google))?$',
                r'(?:தேடு|search)\s+(.+)',
            ],
            'open_app': [
                rf'(?:open|launch|start|run|show|go to)\s+({self.app_list})',
                rf'({self.app_list})\s+(?:open|திற|ஓபன்|launch|start)',
                r'(?:open|launch|start|run)\s+(.+)',  # Catch-all for any app
            ],
            'close_app': [
                r'(?:close|exit|quit|stop|kill|end)\s+(.+)',
                r'(?:மூடு|close)\s+(.+)',
            ],
            'volume_up': [
                r'(?:volume|sound)\s+(?:up|increase|higher|louder)',
                r'(?:increase|raise|turn up)\s+(?:the\s+)?(?:volume|sound)',
                r'(?:வால்யூம்|volume)\s+(?:அதிகம்|up)',
                r'louder',
            ],
            'volume_down': [
                r'(?:volume|sound)\s+(?:down|decrease|lower|quieter)',
                r'(?:decrease|reduce|turn down)\s+(?:the\s+)?(?:volume|sound)',
                r'(?:வால்யூம்|volume)\s+(?:குறை|down)',
                r'quieter',
            ],
            'mute': [
                r'(?:mute|silence|unmute)',
                r'toggle\s+mute',
            ],
            'screenshot': [
                r'(?:take|capture|grab)\s+(?:a\s+)?(?:screenshot|screen shot|screen capture)',
                r'screenshot',
            ],
            'shutdown': [
                r'(?:shut down|shutdown|power off|turn off)\s+(?:the\s+)?(?:computer|system|pc)?',
                r'(?:shut down|shutdown)\s+in\s+(\d+)\s+minutes?',
            ],
            'restart': [
                r'(?:restart|reboot)\s+(?:the\s+)?(?:computer|system|pc)?',
            ],
            'lock': [
                r'lock\s+(?:the\s+)?(?:screen|computer|pc)?',
            ],
            'whatsapp_message': [
                r'(?:whatsapp|send message to)\s+(.+)',
                r'message\s+(.+?)\s+(?:on whatsapp)?',
            ],
            'time': [
                r'(?:what|tell|what\'s)\s+(?:is\s+)?(?:the\s+)?(?:current\s+)?time',
                r'(?:என்ன|time)\s+(?:நேரம்|time)',
                r'time\s+(?:now|please)',
            ],
            'date': [
                r'(?:what|tell|what\'s)\s+(?:is\s+)?(?:the\s+)?(?:today\'?s?\s+)?date',
                r'(?:என்ன|what)\s+(?:தேதி|date)',
                r'(?:what|which)\s+day\s+(?:is\s+)?(?:it|today)',
            ],
            'system_info': [
                r'(?:system|pc|computer)\s+(?:status|info|information|stats)',
                r'(?:how|what)\s+(?:is|are)\s+(?:my\s+)?(?:system|computer)\s+(?:doing|status)',
                r'(?:check|show|get)\s+(?:system|pc)\s+(?:status|info|stats)',
            ],
            'memory_info': [
                r'(?:memory|ram)\s+(?:status|info|usage|stats)',
                r'(?:how much|check|show)\s+(?:memory|ram)\s+(?:is\s+)?(?:used|available|free)?',
                r'(?:ram|memory)\s+(?:usage|status)',
            ],
            'disk_info': [
                r'(?:disk|storage|drive|hard drive|ssd)\s+(?:status|info|usage|space|stats)',
                r'(?:how much|check|show)\s+(?:disk|storage)\s+(?:space|is\s+)?(?:used|available|free)?',
                r'(?:storage|disk)\s+(?:usage|status|space)',
            ],
            'battery_info': [
                r'(?:battery|power)\s+(?:status|info|level|percentage|stats)',
                r'(?:how much|check|show)\s+(?:battery|power)\s+(?:is\s+)?(?:left|remaining)?',
                r'(?:battery|power)\s+(?:percentage|level)',
            ],
        }
    
    def parse(self, command):
        """
        Parse command and extract intent
        
        Args:
            command: User command string
        
        Returns:
            dict: Intent with action and parameters
        """
        command_lower = command.lower().strip()
        
        # Check each pattern
        for action, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_lower)
                if match:
                    # Extract parameters
                    params = {}
                    if match.groups():
                        if action == 'play_youtube':
                            captured = match.group(1)
                            params['query'] = captured.strip() if captured else ''
                        elif action == 'open_app':
                            captured = match.group(1)
                            params['app'] = captured.strip() if captured else ''
                        elif action == 'close_app':
                            captured = match.group(1)
                            params['app'] = captured.strip() if captured else ''
                        elif action == 'search_google':
                            captured = match.group(1)
                            params['query'] = captured.strip() if captured else ''
                        elif action == 'whatsapp_message':
                            captured = match.group(1)
                            params['contact'] = captured.strip() if captured else ''
                        elif action == 'shutdown':
                            if len(match.groups()) > 0 and match.group(1):
                                params['minutes'] = int(match.group(1))
                            else:
                                params['minutes'] = 0
                    
                    return {
                        'action': action,
                        'params': params,
                        'original': command
                    }
        
        # Default: AI chat
        return {
            'action': 'chat',
            'params': {'message': command},
            'original': command
        }
