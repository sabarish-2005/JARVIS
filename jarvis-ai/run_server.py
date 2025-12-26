"""
==================== JARVIS SERVER RUNNER ====================
Auto-restart wrapper for stable operation
"""

import subprocess
import sys
import time
import os

def run_server():
    """Run the API server with auto-restart on crash"""
    print("=" * 60)
    print("🤖 JARVIS Auto-Restart Server Manager")
    print("=" * 60)
    print("Press Ctrl+C to stop completely")
    print()
    
    restart_count = 0
    max_restarts = 10
    restart_delay = 2  # seconds
    
    while restart_count < max_restarts:
        try:
            print(f"🚀 Starting JARVIS API Server (Attempt {restart_count + 1})...")
            
            # Run the API server
            process = subprocess.Popen(
                [sys.executable, "api_server.py"],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=sys.stdout,
                stderr=sys.stderr
            )
            
            # Wait for the process to complete
            process.wait()
            
            exit_code = process.returncode
            
            if exit_code == 0:
                print("✅ Server stopped gracefully")
                break
            else:
                print(f"⚠️ Server crashed with exit code: {exit_code}")
                restart_count += 1
                
                if restart_count < max_restarts:
                    print(f"🔄 Restarting in {restart_delay} seconds...")
                    time.sleep(restart_delay)
                    # Increase delay for subsequent restarts (backoff)
                    restart_delay = min(restart_delay * 1.5, 30)
                else:
                    print("❌ Max restarts reached. Please check the server logs.")
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping JARVIS server...")
            if process:
                process.terminate()
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            restart_count += 1
            time.sleep(restart_delay)
    
    print("👋 JARVIS server shutdown complete")

if __name__ == "__main__":
    run_server()
