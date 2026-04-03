import re
import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT FIX ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Running')

def run_port_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# --- CONFIGURATION ---
API_ID = 32153130
API_HASH = '66168465c6360e3d856a8a53a3d21e84'
SESSION_STRING = '1BZWaqwUBu54l2KPxOFDkpU-V7HDwr7Nutf7QUfvqScZTiMz_5eY3xkUu4DJLsTV-O1Jx9xxEWVy7Z4N5Q5pI8vokCMEbJSBRFRgOCB5tI4LLdS8msRAqd3X8vH5ZWGe083VuLUMx0Y5mqTG7sZoffY9uB4iJQ4HsDoeflz-V0h82KdfuycU3gnSFgfXN5VkD0oV9oIyZRzIzctMnmOHVOL6vJa6n-rE2dCDKPbtuH3Nh-1imt0ecXMo1579xBIXNY6M06CsmYuDl5rmJO1ZdsTlheYa7OnCVwch0XPEnWfrlo2psk7yYFaxSIrt4Yq0IBJ-7JG1nxxJXNw0AJNR3jz_Px4mPcR4='

SOURCE_CHANNEL = -1002609048662 
TARGET_CHANNEL = '@onexbet_1xbet7'

def clean_and_filter(text):
    if not text:
        return ""
    
    # Check for Winning Ticket
    if any(x in text.lower() for x in ['paid out', 'won', 'gagné', 'payé']):
        return "WON✅"
    
    # Remove Non-ASCII (Emojis)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Remove Links and Usernames
    text = re.sub(r'https?://\S+|t\.me/\S+|@[\w\d_]+', '', text)
    
    # Extract Betting Code (Uppercase + Numbers, 5-7 chars)
    codes = re.findall(r'\b[A-Z0-9]{5,7}\b', text)
    if codes:
        return codes[0]
        
    return ""

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    # Only process messages with media (Photo/File)
    if not event.media:
        return

    processed_text = clean_and_filter(event.raw_text)
    
    try:
        await client.send_message(TARGET_CHANNEL, processed_text, file=event.media)
        print(f"Success: {processed_text}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    Thread(target=run_port_server, daemon=True).start()
    await client.start()
    print("🚀 Bot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
