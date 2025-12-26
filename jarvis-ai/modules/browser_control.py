"""
==================== BROWSER CONTROL MODULE ====================
Real browser automation using Playwright
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
from rich.console import Console

console = Console()

class BrowserController:
    """Controls web browser with full automation"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, *args):
        """Context manager exit"""
        self.close()
    
    def start(self):
        """Start browser"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            self.page = self.context.new_page()
            console.print("[green]🌐 Browser started[/green]")
        except Exception as e:
            console.print(f"[red]Browser start error: {e}[/red]")
            raise
    
    def close(self):
        """Close browser"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            console.print("[yellow]Browser closed[/yellow]")
        except:
            pass
    
    def goto(self, url):
        """Navigate to URL"""
        try:
            self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(2)  # Wait for page to stabilize
            return True
        except Exception as e:
            console.print(f"[red]Navigation error: {e}[/red]")
            return False
    
    def click(self, selector):
        """Click element"""
        try:
            self.page.click(selector, timeout=10000)
            time.sleep(1)
            return True
        except Exception as e:
            console.print(f"[red]Click error: {e}[/red]")
            return False
    
    def type_text(self, selector, text):
        """Type text into element"""
        try:
            self.page.fill(selector, text)
            time.sleep(0.5)
            return True
        except Exception as e:
            console.print(f"[red]Type error: {e}[/red]")
            return False
    
    def press_key(self, key):
        """Press keyboard key"""
        try:
            self.page.keyboard.press(key)
            time.sleep(0.5)
            return True
        except Exception as e:
            console.print(f"[red]Key press error: {e}[/red]")
            return False
    
    def youtube_play(self, query):
        """
        Open YouTube and play first video matching query
        
        COMPLETE AUTOMATION - NO USER INTERACTION NEEDED
        """
        try:
            console.print(f"[cyan]Opening YouTube: {query}[/cyan]")
            
            # 1. Go to YouTube
            self.goto("https://www.youtube.com")
            
            # 2. Click search box
            self.page.click('input[name="search_query"]')
            
            # 3. Type search query
            self.page.fill('input[name="search_query"]', query)
            
            # 4. Press Enter to search
            self.page.keyboard.press('Enter')
            time.sleep(3)  # Wait for results
            
            # 5. Click first video thumbnail
            try:
                # Method 1: Click first video renderer
                self.page.click('ytd-video-renderer:first-child a#thumbnail', timeout=5000)
            except:
                # Method 2: Click any video thumbnail
                self.page.click('a#video-title', timeout=5000)
            
            time.sleep(2)  # Wait for video page
            
            # 6. Try to click play button if needed
            try:
                self.page.click('button.ytp-large-play-button', timeout=3000)
            except:
                # Video might autoplay
                pass
            
            console.print("[green]✅ YouTube video playing[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]YouTube error: {e}[/red]")
            return False
    
    def google_search(self, query):
        """Perform Google search"""
        try:
            console.print(f"[cyan]Searching Google: {query}[/cyan]")
            
            # Navigate to Google
            self.goto("https://www.google.com")
            
            # Type in search box
            self.page.fill('textarea[name="q"]', query)
            
            # Press Enter
            self.page.keyboard.press('Enter')
            
            time.sleep(2)
            console.print("[green]✅ Google search completed[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Google search error: {e}[/red]")
            return False
    
    def whatsapp_send_message(self, contact_name, message):
        """
        Send WhatsApp message via WhatsApp Web
        
        COMPLETE AUTOMATION
        """
        try:
            console.print(f"[cyan]Opening WhatsApp Web for: {contact_name}[/cyan]")
            
            # 1. Go to WhatsApp Web
            self.goto("https://web.whatsapp.com")
            
            # Wait for QR code scan or auto-login
            console.print("[yellow]Waiting for WhatsApp Web to load...[/yellow]")
            try:
                # Wait for main chat panel (means logged in)
                self.page.wait_for_selector('div[role="textbox"]', timeout=30000)
            except:
                console.print("[red]WhatsApp Web not logged in. Please scan QR code.[/red]")
                return False
            
            # 2. Search for contact
            search_box = self.page.locator('div[contenteditable="true"][data-tab="3"]')
            search_box.click()
            search_box.fill(contact_name)
            time.sleep(2)
            
            # 3. Click first result
            try:
                self.page.click(f'span[title="{contact_name}"]', timeout=5000)
            except:
                # Try clicking any first contact
                self.page.click('div[data-testid="cell-frame-container"]:first-child', timeout=5000)
            
            time.sleep(1)
            
            # 4. Type message
            message_box = self.page.locator('div[contenteditable="true"][data-tab="10"]')
            message_box.click()
            message_box.fill(message)
            
            # 5. Send message
            self.page.keyboard.press('Enter')
            
            console.print(f"[green]✅ Message sent to {contact_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]WhatsApp error: {e}[/red]")
            return False
