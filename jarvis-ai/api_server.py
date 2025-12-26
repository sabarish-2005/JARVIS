"""
==================== JARVIS API SERVER ====================
Flask API for React Frontend Integration
Serves React frontend + API from single Python process
"""

from flask import Flask, request, jsonify, Response, send_from_directory, send_file
from flask_cors import CORS
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import subprocess
import webbrowser
import threading
import time

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))

# Import JARVIS modules (with fallbacks for missing dependencies)
try:
    from voice_engine import VoiceEngine
except ImportError as e:
    print(f"⚠️ Could not import VoiceEngine: {e}")
    VoiceEngine = None

try:
    from intent_parser import IntentParser
except ImportError as e:
    print(f"⚠️ Could not import IntentParser: {e}")
    IntentParser = None

try:
    from action_executor import ActionExecutor
except ImportError as e:
    print(f"⚠️ Could not import ActionExecutor: {e}")
    ActionExecutor = None

try:
    from ai_brain import AIBrain
except ImportError as e:
    print(f"⚠️ Could not import AIBrain: {e}")
    AIBrain = None

# Workspace roots and helpers for safe file access
ROOT_DIR = Path(__file__).parent.resolve()
WEB_DIR = ROOT_DIR / "web"
FRONTEND_DIR = ROOT_DIR.parent / "jarvis-frontend"
FRONTEND_DIST = FRONTEND_DIR / "dist"

# Check multiple possible dist locations (for Render deployment)
if not FRONTEND_DIST.exists():
    # Try relative to repo root (Render builds from repo root)
    alt_dist = ROOT_DIR.parent / "jarvis-frontend" / "dist"
    if alt_dist.exists():
        FRONTEND_DIST = alt_dist

EXCLUDED_DIRS = {'.git', '.venv', '__pycache__', '.vscode'}


def _resolve_safe_path(relative_path: str) -> Path:
    """Resolve a user-supplied path safely within ROOT_DIR."""
    target = (ROOT_DIR / relative_path).resolve()
    if target == ROOT_DIR:
        return target
    if ROOT_DIR in target.parents:
        return target
    raise ValueError("Invalid path")


def _serialize_entry(path: Path) -> dict:
    """Convert a filesystem entry to JSON-serializable dict."""
    return {
        'name': path.name,
        'path': str(path.relative_to(ROOT_DIR)),
        'type': 'dir' if path.is_dir() else 'file',
        'size': path.stat().st_size if path.is_file() else None,
        'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
    }

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize JARVIS components with fallbacks
print("🚀 Initializing JARVIS API Server...")

voice_engine = None
intent_parser = None
action_executor = None
ai_brain = None

try:
    voice_engine = VoiceEngine() if VoiceEngine else None
except Exception as e:
    print(f"⚠️ Voice engine failed: {e}")
    voice_engine = None

try:
    intent_parser = IntentParser() if IntentParser else None
except Exception as e:
    print(f"⚠️ Intent parser failed: {e}")
    intent_parser = None

try:
    action_executor = ActionExecutor() if ActionExecutor else None
except Exception as e:
    print(f"⚠️ Action executor failed: {e}")
    action_executor = None

try:
    ai_brain = AIBrain() if AIBrain else None
except Exception as e:
    print(f"⚠️ AI brain failed: {e}")
    ai_brain = None

print("✅ JARVIS components initialized (with fallbacks for unavailable features)")


# ==================== BUILD FRONTEND ====================

def build_frontend():
    """Build React frontend if needed"""
    # Check if dist folder exists first
    index_html = FRONTEND_DIST / "index.html"
    
    if index_html.exists():
        print("✅ Frontend already built")
        return True
    
    # Skip building on Render - it should be built during deploy phase
    if os.environ.get('RENDER'):
        print("⚠️ Frontend not found on Render - build may have failed")
        return False
    
    if not FRONTEND_DIR.exists():
        print("⚠️ Frontend directory not found at:", FRONTEND_DIR)
        return False
    
    print("📦 Building React frontend locally...")
    try:
        # Detect available package manager
        npm_cmd = "npm"
        for cmd in ["npm", "bun", "yarn"]:
            try:
                result = subprocess.run([cmd, "--version"], capture_output=True, check=True, shell=True)
                npm_cmd = cmd
                break
            except:
                continue
        
        print(f"Using package manager: {npm_cmd}")
        
        # Install dependencies if needed
        node_modules = FRONTEND_DIR / "node_modules"
        if not node_modules.exists():
            print("📥 Installing dependencies...")
            subprocess.run(
                [npm_cmd, "install"],
                cwd=str(FRONTEND_DIR),
                shell=True,
                check=True
            )
        
        # Build the frontend
        print("🔨 Running build...")
        subprocess.run(
            [npm_cmd, "run", "build"],
            cwd=str(FRONTEND_DIR),
            shell=True,
            check=True
        )
        print("✅ Frontend built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


# ==================== SERVE REACT FRONTEND ====================

@app.route('/')
def serve_frontend():
    """Serve React frontend index.html"""
    if FRONTEND_DIST.exists():
        return send_from_directory(str(FRONTEND_DIST), 'index.html')
    else:
        return jsonify({
            'message': 'JARVIS API Server',
            'frontend': 'Not built. Run: cd jarvis-frontend && npm run build',
            'api': '/api/health'
        })


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from React build"""
    # First check if it's an API route
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    # Try to serve the file from dist
    if FRONTEND_DIST.exists():
        file_path = FRONTEND_DIST / path
        if file_path.exists() and file_path.is_file():
            return send_from_directory(str(FRONTEND_DIST), path)
        else:
            # For React Router - serve index.html for any unmatched routes
            return send_from_directory(str(FRONTEND_DIST), 'index.html')
    
    return jsonify({'error': 'Not found'}), 404


@app.route('/assets/<path:path>')
def serve_assets(path):
    """Serve assets from React build"""
    if FRONTEND_DIST.exists():
        return send_from_directory(str(FRONTEND_DIST / 'assets'), path)
    return jsonify({'error': 'Not found'}), 404


# ==================== HEALTH & STATUS ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check API health status"""
    return jsonify({
        'status': 'online',
        'message': 'JARVIS API Server is running',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get JARVIS system status"""
    # Check voice engine capabilities
    voice_status = 'unavailable'
    try:
        if voice_engine and hasattr(voice_engine, 'listen') and hasattr(voice_engine, 'speak'):
            voice_status = 'ready'
    except:
        voice_status = 'unavailable'
    
    return jsonify({
        'status': 'operational',
        'components': {
            'voice_engine': voice_status,
            'intent_parser': 'ready',
            'action_executor': 'ready',
            'ai_brain': 'ready' if ai_brain and ai_brain.client else 'limited'
        },
        'wake_word': 'jarvis',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/system-stats', methods=['GET'])
def get_system_stats():
    """Get live system statistics (CPU, RAM, Battery, etc.)"""
    import psutil
    
    try:
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        # Memory info
        memory = psutil.virtual_memory()
        ram_percent = memory.percent
        ram_total = round(memory.total / (1024**3), 1)  # GB
        ram_used = round(memory.used / (1024**3), 1)  # GB
        
        # Disk info
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_total = round(disk.total / (1024**3), 1)  # GB
        disk_used = round(disk.used / (1024**3), 1)  # GB
        
        # Battery info (if available)
        battery_percent = None
        battery_charging = None
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_percent = battery.percent
                battery_charging = battery.power_plugged
        except:
            pass
        
        # Network info
        net_io = psutil.net_io_counters()
        bytes_sent = round(net_io.bytes_sent / (1024**2), 1)  # MB
        bytes_recv = round(net_io.bytes_recv / (1024**2), 1)  # MB
        
        return jsonify({
            'success': True,
            'cpu': {
                'percent': cpu_percent,
                'cores': cpu_count
            },
            'memory': {
                'percent': ram_percent,
                'total_gb': ram_total,
                'used_gb': ram_used
            },
            'disk': {
                'percent': disk_percent,
                'total_gb': disk_total,
                'used_gb': disk_used
            },
            'battery': {
                'percent': battery_percent,
                'charging': battery_charging
            } if battery_percent is not None else None,
            'network': {
                'sent_mb': bytes_sent,
                'recv_mb': bytes_recv
            },
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== AI & CHAT ENDPOINTS ====================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to JARVIS AI"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        response = ai_brain.chat(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/command', methods=['POST'])
def execute_command():
    """Execute a JARVIS command"""
    try:
        data = request.get_json() or {}
        command = data.get('command', '')
        
        if command:
            command = command.strip()
        
        if not command:
            return jsonify({
                'success': False,
                'error': 'Command is required'
            }), 400
        
        # Check if intent parser is available
        if not intent_parser:
            return jsonify({
                'success': False,
                'error': 'Intent parser not available'
            }), 503
        
        # Parse the command to get intent
        intent = intent_parser.parse(command)
        
        if intent['action'] == 'unknown':
            return jsonify({
                'success': False,
                'error': 'Command not recognized',
                'command': command
            }), 400
        
        # Check if action executor is available
        if not action_executor:
            return jsonify({
                'success': False,
                'error': 'Action executor not available'
            }), 503
        
        # Execute the action
        result = action_executor.execute(intent)
        
        return jsonify({
            'success': result.get('success', True),
            'command': command,
            'action': intent['action'],
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== VOICE ENDPOINTS ====================

@app.route('/api/listen', methods=['POST'])
def listen():
    """Listen for voice input and return transcript"""
    try:
        # Check if voice engine is available
        if not voice_engine or not hasattr(voice_engine, 'listen'):
            return jsonify({
                'success': False,
                'error': 'Voice recognition is not available on this system'
            }), 503
        
        # Get audio timeout from request
        data = request.get_json() or {}
        timeout = data.get('timeout', 5)  # Default 5 seconds
        # Also accept 'duration' for backwards compatibility
        if 'duration' in data:
            timeout = data['duration']
        
        wake_word_mode = data.get('wake_word', False)
        
        transcript = voice_engine.listen(timeout=timeout)
        
        if not transcript:
            return jsonify({
                'success': False,
                'error': 'No audio detected'
            }), 400
        
        # Check if wake word detected
        if transcript and wake_word_mode:
            transcript_lower = transcript.lower()
            wake_words = ['jarvis', 'hey jarvis', 'ok jarvis']
            has_wake_word = any(word in transcript_lower for word in wake_words)
            
            return jsonify({
                'success': True,
                'transcript': transcript,
                'wake_word_detected': has_wake_word,
                'timestamp': datetime.now().isoformat()
            }), 200
        
        return jsonify({
            'success': True,
            'transcript': transcript,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except AttributeError as e:
        return jsonify({
            'success': False,
            'error': 'Voice recognition feature is not properly configured'
        }), 503
    except Exception as e:
        print(f"Voice listen error: {e}")
        return jsonify({
            'success': False,
            'error': f'Voice recognition error: {str(e)}'
        }), 500


@app.route('/api/speak', methods=['POST'])
def speak():
    """Convert text to speech"""
    try:
        # Check if voice engine is available
        if not voice_engine or not hasattr(voice_engine, 'speak'):
            return jsonify({
                'success': False,
                'error': 'Text-to-speech is not available on this system'
            }), 503
        
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        voice_engine.speak(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except AttributeError as e:
        return jsonify({
            'success': False,
            'error': 'Text-to-speech feature is not properly configured'
        }), 503
    except Exception as e:
        print(f"Voice speak error: {e}")
        return jsonify({
            'success': False,
            'error': f'Text-to-speech error: {str(e)}'
        }), 500


# ==================== INTENT PARSING ENDPOINTS ====================

@app.route('/api/parse', methods=['POST'])
def parse_command():
    """Parse a command and return the intent"""
    try:
        data = request.get_json()
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({
                'success': False,
                'error': 'Command is required'
            }), 400
        
        intent = intent_parser.parse(command)
        
        return jsonify({
            'success': True,
            'command': command,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== SUPPORTED ACTIONS ENDPOINT ====================

@app.route('/api/actions', methods=['GET'])
def get_supported_actions():
    """Get list of supported actions"""
    actions = [
        'play_youtube',
        'search_google',
        'open_app',
        'close_app',
        'volume_up',
        'volume_down',
        'mute',
        'screenshot',
        'shutdown',
        'restart',
        'lock',
        'whatsapp_message',
        'time',
        'date',
        'chat'
    ]
    
    return jsonify({
        'success': True,
        'total': len(actions),
        'actions': actions,
        'timestamp': datetime.now().isoformat()
    }), 200


# ==================== SYSTEM CONTROL ENDPOINTS ====================

@app.route('/api/system/volume', methods=['POST'])
def control_volume():
    """Control system volume"""
    try:
        data = request.get_json()
        action = data.get('action', '').lower()  # 'up', 'down', 'mute', 'unmute'
        level = data.get('level')  # Optional: 0-100
        
        if action == 'up':
            result = action_executor._volume_up()
        elif action == 'down':
            result = action_executor._volume_down()
        elif action == 'mute':
            result = action_executor._mute()
        elif action == 'set' and level is not None:
            # Set to specific level (if available)
            result = {'success': True, 'message': f'Volume set to {level}%'}
        else:
            return jsonify({'success': False, 'error': 'Invalid action'}), 400
        
        return jsonify({
            'success': True,
            'action': action,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/system/screenshot', methods=['POST'])
def take_screenshot():
    """Take a screenshot"""
    try:
        result = action_executor._screenshot()
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/system/lock', methods=['POST'])
def lock_system():
    """Lock the system"""
    try:
        result = action_executor._lock()
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/system/shutdown', methods=['POST'])
def shutdown_system():
    """Shutdown the system"""
    try:
        data = request.get_json()
        delay = data.get('delay', 0)  # Delay in seconds
        
        result = action_executor._shutdown({'delay': delay})
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/system/restart', methods=['POST'])
def restart_system():
    """Restart the system"""
    try:
        result = action_executor._restart()
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== BROWSER CONTROL ENDPOINTS ====================

@app.route('/api/browser/youtube', methods=['POST'])
def youtube_search():
    """Search and play on YouTube"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        result = action_executor._play_youtube({'query': query})
        
        return jsonify({
            'success': True,
            'query': query,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/browser/google', methods=['POST'])
def google_search():
    """Search on Google"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        result = action_executor._search_google({'query': query})
        
        return jsonify({
            'success': True,
            'query': query,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== UTILITY ENDPOINTS ====================

@app.route('/api/time', methods=['GET'])
def get_time():
    """Get current system time"""
    try:
        result = action_executor._tell_time()
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/date', methods=['GET'])
def get_date():
    """Get current system date"""
    try:
        result = action_executor._tell_date()
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== FILE BROWSER ENDPOINTS ====================

@app.route('/api/files', methods=['GET'])
def list_files():
        """List files in the workspace (read-only)."""
        rel_path = request.args.get('path', '').strip()

        try:
                target = _resolve_safe_path(rel_path or '.')
        except ValueError:
                return jsonify({'success': False, 'error': 'Invalid path'}), 400

        if not target.exists():
                return jsonify({'success': False, 'error': 'Path not found'}), 404

        # If a file is requested, return its metadata only
        if target.is_file():
                return jsonify({
                        'success': True,
                        'entry': _serialize_entry(target),
                        'timestamp': datetime.now().isoformat()
                }), 200

        entries = []
        for item in sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
                if item.name in EXCLUDED_DIRS or item.name.startswith('.git'):
                        continue
                entries.append(_serialize_entry(item))

        return jsonify({
                'success': True,
                'path': str(target.relative_to(ROOT_DIR)),
                'entries': entries,
                'timestamp': datetime.now().isoformat()
        }), 200


@app.route('/files', methods=['GET'])
def files_page():
    """Lightweight web UI for browsing project files."""
    html = f"""<!doctype html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>JARVIS Project Files</title>
    <style>
        body {{ font-family: Arial, sans-serif; background:#0b1220; color:#eef1f7; margin:0; padding:0; }}
        header {{ padding:16px 20px; background:#10182f; border-bottom:1px solid #1d2a46; }}
        h1 {{ margin:0; font-size:18px; letter-spacing:0.5px; }}
        #container {{ padding:16px 20px; }}
        #path {{ color:#8fb2ff; font-weight:600; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:12px; margin-top:12px; }}
        .card {{ background:#111a30; border:1px solid #1e2c4f; border-radius:8px; padding:12px; cursor:pointer; transition:border 0.2s, transform 0.1s; }}
        .card:hover {{ border-color:#3b82f6; transform:translateY(-1px); }}
        .label {{ display:inline-block; padding:2px 6px; border-radius:4px; font-size:12px; background:#1e2c4f; color:#9fb7ff; margin-bottom:6px; }}
        .name {{ font-weight:700; font-size:15px; word-break:break-all; }}
        .meta {{ font-size:12px; color:#9ca7c7; margin-top:6px; }}
        button {{ background:#1e2c4f; color:#dce7ff; border:1px solid #2b3b63; border-radius:6px; padding:6px 10px; cursor:pointer; }}
        button:hover {{ border-color:#3b82f6; }}
    </style>
</head>
<body>
    <header>
        <h1>JARVIS Project Files</h1>
    </header>
    <div id='container'>
        <div>
            <span>Current path: </span><span id='path'></span>
            <div style='margin-top:8px;'>
                <button id='upBtn'>Go Up</button>
                <button id='rootBtn'>Go Root</button>
            </div>
        </div>
        <div class='grid' id='grid'></div>
    </div>
    <script>
        const pathEl = document.getElementById('path');
        const gridEl = document.getElementById('grid');
        const upBtn = document.getElementById('upBtn');
        const rootBtn = document.getElementById('rootBtn');

        let currentPath = '';

        async function load(path='') {{
            const res = await fetch(`/api/files?path=${{encodeURIComponent(path)}}`);
            const data = await res.json();
            if (!data.success) {{
                alert(data.error || 'Failed to load');
                return;
            }}
            currentPath = data.path || '';
            pathEl.textContent = currentPath || '.';
            renderCards(data.entries || []);
        }}

        function renderCards(entries) {{
            gridEl.innerHTML = '';
            entries.forEach(entry => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => handleClick(entry);
                card.innerHTML = `
                    <div class='label'>${{entry.type === 'dir' ? 'DIR' : 'FILE'}}</div>
                    <div class='name'>${{entry.name}}</div>
                    <div class='meta'>${{entry.modified || ''}}</div>
                    <div class='meta'>${{entry.type === 'file' && entry.size != null ? (entry.size + ' bytes') : ''}}</div>
                `;
                gridEl.appendChild(card);
            }});
        }}

        function handleClick(entry) {{
            if (entry.type === 'dir') {{
                const next = currentPath ? `${{currentPath}}/${{entry.name}}` : entry.name;
                load(next);
            }}
        }}

        upBtn.onclick = () => {{
            if (!currentPath) return;
            const parts = currentPath.split('/').filter(Boolean);
            parts.pop();
            load(parts.join('/'));
        }};

        rootBtn.onclick = () => load('');

        load('');
    </script>
</body>
</html>"""
    return Response(html, mimetype='text/html')


# ==================== FRONTEND (STATIC) ====================

@app.route('/app', methods=['GET'])
def serve_frontend_root():
    """Serve the static frontend index."""
    if not (WEB_DIR / 'index.html').exists():
        return jsonify({'success': False, 'error': 'Frontend not found'}), 404
    return send_from_directory(WEB_DIR, 'index.html')


@app.route('/web/<path:filename>', methods=['GET'])
def serve_frontend_assets(filename):
    """Serve static assets from the web directory."""
    target = WEB_DIR / filename
    if not target.exists():
        return jsonify({'success': False, 'error': 'File not found'}), 404
    return send_from_directory(WEB_DIR, filename)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'path': request.path
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'method': request.method
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ==================== MAIN ====================

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 JARVIS AI System Starting...")
    print("="*50)
    
    # Build frontend if needed
    build_frontend()
    
    print("\n" + "="*50)
    print("🌐 JARVIS running at: http://localhost:5000")
    print("📚 API available at: http://localhost:5000/api")
    print("🎤 Voice commands ready!")
    print("="*50 + "\n")
    
    # Open browser automatically
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run the Flask app with use_reloader=False to prevent double initialization crashes
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Disable debug mode for stability
        threaded=True,
        use_reloader=False  # Prevent reloader from causing issues
    )
