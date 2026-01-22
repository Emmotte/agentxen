#!/usr/bin/env python3
"""
AgentXen Native Messaging Host
Bridges Firefox extension with Python agent using Ollama
"""

import sys
import json
import struct
import asyncio
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from agent import AgentXenController

# Configure logging
logging.basicConfig(
    filename='/tmp/agentxen-native.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NativeMessagingHost:
    """Native messaging host for browser extension"""
    
    def __init__(self):
        self.controller = None
        logging.info("Native messaging host initialized")
    
    async def initialize_agent(self):
        """Initialize the agent controller"""
        self.controller = AgentXenController(model_name="gemma:1b")
        success = await self.controller.initialize()
        if success:
            self.send_message({
                'type': 'status',
                'message': 'Agent initialized successfully'
            })
            return True
        else:
            self.send_message({
                'type': 'error',
                'message': 'Failed to initialize agent'
            })
            return False
    
    def read_message(self):
        """Read message from stdin (browser extension)"""
        try:
            # Read message length (4 bytes)
            raw_length = sys.stdin.buffer.read(4)
            if len(raw_length) == 0:
                return None
            
            message_length = struct.unpack('=I', raw_length)[0]
            
            # Read the message
            message = sys.stdin.buffer.read(message_length).decode('utf-8')
            return json.loads(message)
        except Exception as e:
            logging.error(f"Error reading message: {e}")
            return None
    
    def send_message(self, message):
        """Send message to stdout (browser extension)"""
        try:
            encoded_message = json.dumps(message).encode('utf-8')
            encoded_length = struct.pack('=I', len(encoded_message))
            
            sys.stdout.buffer.write(encoded_length)
            sys.stdout.buffer.write(encoded_message)
            sys.stdout.buffer.flush()
            
            logging.debug(f"Sent message: {message}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")
    
    async def handle_command(self, command_text, tab_id=None):
        """Process a command from the browser"""
        logging.info(f"Handling command: {command_text}")
        
        if not self.controller:
            await self.initialize_agent()
        
        if not self.controller:
            self.send_message({
                'type': 'error',
                'message': 'Agent not initialized'
            })
            return
        
        # Send status update
        self.send_message({
            'type': 'status',
            'message': f'Processing: {command_text}'
        })
        
        # Process command
        try:
            result = await self.controller.process_command(command_text)
            
            if result['status'] == 'success':
                self.send_message({
                    'type': 'result',
                    'success': True,
                    'message': f"Executed {len(result['results'])} actions",
                    'data': result
                })
            else:
                self.send_message({
                    'type': 'result',
                    'success': False,
                    'message': result.get('error', 'Unknown error')
                })
        except Exception as e:
            logging.error(f"Error processing command: {e}")
            self.send_message({
                'type': 'error',
                'message': str(e)
            })
    
    async def run(self):
        """Main message loop"""
        logging.info("Native messaging host started")
        
        # Initialize agent
        await self.initialize_agent()
        
        # Message loop
        while True:
            try:
                message = await asyncio.get_event_loop().run_in_executor(
                    None, self.read_message
                )
                
                if message is None:
                    logging.info("Connection closed")
                    break
                
                logging.debug(f"Received message: {message}")
                
                if message.get('type') == 'command':
                    command_text = message.get('command', {}).get('text', '')
                    tab_id = message.get('tabId')
                    await self.handle_command(command_text, tab_id)
                
            except Exception as e:
                logging.error(f"Error in message loop: {e}")
                break
        
        # Cleanup
        if self.controller:
            await self.controller.cleanup()
        
        logging.info("Native messaging host stopped")

async def main():
    host = NativeMessagingHost()
    await host.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
