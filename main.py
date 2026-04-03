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
        self.send_response(200); self.end_headers()
        self.wfile.write(b'Bot is Running')

def run_port_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleHTTPRequestHandler)
    server.serve_forever()

# --- CONFIGURATION ---
API_ID = 32153130
API_HASH = '66168465c6360e3d856a8a53a3d21e84'

# သင့်ရဲ့ QR နဲ့ရလာတဲ့ String ကို အောက်က ' ' ထဲမှာ သေချာထည့်ပါ
# အစနဲ့အဆုံးမှာ Space (ဟာကွက်) မပါအောင် သတိထားပါ
MY_STR = '1BZWaqwUBu4ioYJx7d-ivKN3BcBp3jaE7ydI3LpFxbcmcKxr8nNlrbCl0KbWyHUkpDIg38xkh1As6tnxppFNDLaz3r6GjCkciq-yRcWl30RW4nz7quowo-Hdld4SA1hgz3OEie5F6Eo4jAvQsJuLTrvNpbeHhK8DjZ184fE1nV9AHOZolqBjUgGJgj89d8qDL32gPrntXRIKlP4UbIZsD0JlqmzC_0fJhQfzG7qVcFp7ttrCo0WXX09h8xgGDKx_yfmlumE0AwYKY6QuZ7NUDHf_iTkXrhs8_2H82hU1SHvzEKACqPSzQTBj0oGyMEjAJjpWW8HsAxnShsx7rszj254vHXH9nVYs='

SOURCE_CH = -1002609048662 
TARGET_CH = '@onexbet_1xbet7'

posted_codes = {}

# --- BOT CLIENT ---
client = TelegramClient(StringSession(MY_STR), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CH))
async def handler(event):
    global posted_codes
    if not event.media: return

    raw_text = event.raw_text
    clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')
    codes = re.findall(r'\b[A-Z0-9]{5,8}\b', clean_text)
    found_code = codes[0] if codes else None
    
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne'])

    try:
        if is_won:
            reply_id = posted_codes.get(found_code) if found_code else None
            await client.send_message(TARGET_CH, "BOOM ✅", file=event.media, reply_to=reply_id)
        elif found_code:
            sent_msg = await client.send_message(TARGET_CH, found_code, file=event.media)
            posted_codes[found_code] = sent_msg.id
    except Exception as e:
        print(f"Error: {e}")

async def start_bot():
    try:
        # connect() နဲ့ အရင်ချိတ်ပါမယ်
        await client.connect()
        
        # အကောင့်ဝင်ထားပြီးသား ဟုတ်မဟုတ် စစ်ဆေးပါတယ်
        if not await client.is_user_authorized():
            print("❌ ERROR: SESSION EXPIRED OR INVALID. PLEASE GET NEW QR STRING.")
            return

        print("🚀 BOT IS SUCCESSFULLY ONLINE!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == '__main__':
    # Render အတွက် Port ဖွင့်ပေးခြင်း
    Thread(target=run_port_server, daemon=True).start()
    
    # Bot စတင်ခြင်း
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
