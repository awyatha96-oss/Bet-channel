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
SESSION_STRING = '1BZWaqwUBu4ioYJx7d-ivKN3BcBp3jaE7ydI3LpFxbcmcKxr8nNlrbCl0KbWyHUkpDIg38xkh1As6tnxppFNDLaz3r6GjCkciq-yRcWl30RW4nz7quowo-Hdld4SA1hgz3OEie5F6Eo4jAvQsJuLTrvNpbeHhK8DjZ184fE1nV9AHOZolqBjUgGJgj89d8qDL32gPrntXRIKlP4UbIZsD0JlqmzC_0fJhQfzG7qVcFp7ttrCo0WXX09h8xgGDKx_yfmlumE0AwYKY6QuZ7NUDHf_iTkXrhs8_2H82hU1SHvzEKACqPSzQTBj0oGyMEjAJjpWW8HsAxnShsx7rszj254vHXH9nVYs='

SOURCE_CHANNEL = -1002609048662 
TARGET_CHANNEL = '@onexbet_1xbet7'

# Memory for Smart Reply
posted_codes = {}

def extract_code(text):
    if not text: return None
    clean_text = text.encode('ascii', 'ignore').decode('ascii')
    codes = re.findall(r'\b[A-Z0-9]{5,8}\b', clean_text)
    return codes[0] if codes else None

def is_winning_ss(text):
    if not text: return False
    keywords = ['paid out', 'won', 'gagne', 'paye', 'success', 'boom']
    return any(x in text.lower() for x in keywords)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    global posted_codes
    if not event.media: return
    
    raw_text = event.raw_text
    found_code = extract_code(raw_text)
    
    try:
        # 1. Winning Screenshot Logic
        if is_winning_ss(raw_text):
            reply_id = None
            if found_code and found_code in posted_codes:
                reply_id = posted_codes[found_code]
            
            await client.send_message(
                TARGET_CHANNEL, 
                "BOOM ✅", 
                file=event.media, 
                reply_to=reply_id
            )
            print(f"Posted: WON SS (Reply to: {reply_id})")

        # 2. New Booking Code Logic
        elif found_code:
            sent_msg = await client.send_message(TARGET_CHANNEL, found_code, file=event.media)
            posted_codes[found_code] = sent_msg.id
            print(f"Recorded: {found_code}")

    except Exception as e:
        print(f"Error: {e}")

async def main():
    Thread(target=run_port_server, daemon=True).start()
    try:
        await client.start()
        print("Bot Started Successfully!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
