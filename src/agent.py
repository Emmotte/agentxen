#!/usr/bin/env python3
"""
AgentXen - AI-powered browser agent controller

This is the main entry point for the AgentXen agent service that:
1. Communicates with Ollama for AI inference
2. Translates natural language commands to browser actions
3. Controls Playwright for browser automation
"""

import asyncio
import json
from typing import Dict, List, Any
from ollama import chat
from playwright.async_api import async_playwright, Browser, Page


class AgentXenController:
    """Main controller for the AgentXen browser agent"""
    
    def __init__(self, model_name: str = "gemma:1b"):
        self.model_name = model_name
        self.browser: Browser = None
        self.pages: Dict[str, Page] = {}
        self.conversation_history: List[Dict] = []
        
    async def initialize(self):
        """Initialize browser and connections"""
        print(f"🚀 Initializing AgentXen with model: {self.model_name}")
        
        # Check if Ollama is available
        try:
            response = chat(model=self.model_name, messages=[
                {'role': 'user', 'content': 'Hello'}
            ])
            print(f"✅ Ollama connection established")
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            print("Please ensure Ollama is installed and running:")
            print("  1. Install: https://ollama.com")
            print(f"  2. Pull model: ollama pull {self.model_name}")
            return False
            
        # Initialize Playwright
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.firefox.launch(
                headless=False,  # Visible browser
                args=['--start-maximized']
            )
            print(f"✅ Browser initialized")
            return True
        except Exception as e:
            print(f"❌ Browser initialization failed: {e}")
            return False
    
    async def process_command(self, user_command: str) -> Dict[str, Any]:
        """
        Process a natural language command from the user
        
        Args:
            user_command: Natural language instruction
            
        Returns:
            Dict containing status, actions taken, and response
        """
        print(f"\n💭 Processing: {user_command}")
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_command
        })
        
        # Create prompt for action planning
        system_prompt = """You are a browser automation assistant. Convert user requests into browser actions.

Available actions:
- navigate: Go to a URL
- click: Click an element
- type: Enter text
- extract: Get information from page
- screenshot: Take a screenshot

Respond in JSON format:
{
  "actions": [
    {"type": "navigate", "url": "https://example.com"},
    {"type": "click", "selector": "button.submit"}
  ],
  "explanation": "What you're doing and why"
}
"""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            *self.conversation_history
        ]
        
        try:
            # Get AI response
            response = chat(
                model=self.model_name,
                messages=messages,
                format='json'
            )
            
            action_plan = json.loads(response.message.content)
            print(f"📋 Plan: {action_plan.get('explanation', 'Processing...')}")
            
            # Execute actions
            results = await self.execute_actions(action_plan.get('actions', []))
            
            # Add assistant response to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': response.message.content
            })
            
            return {
                'status': 'success',
                'plan': action_plan,
                'results': results
            }
            
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def execute_actions(self, actions: List[Dict]) -> List[Dict]:
        """Execute a list of browser actions"""
        results = []
        
        # Create a page if we don't have one
        if not self.pages:
            page = await self.browser.new_page()
            self.pages['main'] = page
        
        page = self.pages.get('main')
        
        for action in actions:
            action_type = action.get('type')
            print(f"⚡ Executing: {action_type}")
            
            try:
                if action_type == 'navigate':
                    url = action.get('url')
                    await page.goto(url)
                    results.append({'action': 'navigate', 'url': url, 'status': 'success'})
                    
                elif action_type == 'click':
                    selector = action.get('selector')
                    await page.click(selector)
                    results.append({'action': 'click', 'selector': selector, 'status': 'success'})
                    
                elif action_type == 'type':
                    selector = action.get('selector')
                    text = action.get('text')
                    await page.fill(selector, text)
                    results.append({'action': 'type', 'status': 'success'})
                    
                elif action_type == 'extract':
                    selector = action.get('selector', 'body')
                    content = await page.text_content(selector)
                    results.append({'action': 'extract', 'content': content[:500], 'status': 'success'})
                    
                elif action_type == 'screenshot':
                    path = action.get('path', 'screenshot.png')
                    await page.screenshot(path=path)
                    results.append({'action': 'screenshot', 'path': path, 'status': 'success'})
                    
            except Exception as e:
                print(f"❌ Action failed: {e}")
                results.append({'action': action_type, 'status': 'error', 'error': str(e)})
        
        return results
    
    async def cleanup(self):
        """Clean up resources"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()


async def main():
    """Main entry point"""
    controller = AgentXenController(model_name="gemma:1b")
    
    if not await controller.initialize():
        return
    
    print("\n" + "="*60)
    print("🌐 AgentXen Browser Agent Ready!")
    print("="*60)
    print("\nExample commands:")
    print("  - Go to google.com and search for AI")
    print("  - Open reddit.com and show me the top posts")
    print("  - Navigate to github.com")
    print("\nType 'quit' to exit\n")
    
    try:
        while True:
            command = input("💬 You: ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                break
                
            if not command:
                continue
            
            result = await controller.process_command(command)
            
            if result['status'] == 'success':
                print(f"✅ Done! Executed {len(result['results'])} actions")
            else:
                print(f"❌ Error: {result.get('error')}")
                
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    finally:
        await controller.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
