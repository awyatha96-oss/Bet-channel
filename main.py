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
MY_SESSION = '1BZWaqwUBu4ioYJx7d-ivKN3BcBp3jaE7ydI3LpFxbcmcKxr8nNlrbCl0KbWyHUkpDIg38xkh1As6tnxppFNDLaz3r6GjCkciq-yRcWl30RW4nz7quowo-Hdld4SA1hgz3OEie5F6Eo4jAvQsJuLTrvNpbeHhK8DjZ184fE1nV9AHOZolqBjUgGJgj89d8qDL32gPrntXRIKlP4UbIZsD0JlqmzC_0fJhQfzG7qVcFp7ttrCo0WXX09h8xgGDKx_yfmlumE0AwYKY6QuZ7NUDHf_iTkXrhs8_2H82hU1SHvzEKACqPSzQTBj0oGyMEjAJjpWW8HsAxnShsx7rszj254vHXH9nVYs='

SOURCE_CHANNEL = -1002609048662 
TARGET_CHANNEL = '@onexbet_1xbet7'

posted_codes = {}

client = TelegramClient(StringSession(MY_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    global posted_codes
    if not event.media: return

    raw_text = event.raw_text
    
    # Booking Code ရှာဖွေခြင်း
    clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')
    codes = re.findall(r'\b[A-Z0-9]{5,8}\b', clean_text)
    found_code = codes[0] if codes else None
    
    # နိုင်တဲ့ပုံ ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne'])

    try:
        if is_won:
            # နိုင်တဲ့ပုံဆိုရင် Code တူတဲ့ Post ကို Reply ထောက်မယ်
            reply_id = posted_codes.get(found_code) if found_code else None
            await client.send_message(TARGET_CHANNEL, "BOOM ✅", file=event.media, reply_to=reply_id)
            print(f"✅ Won SS Sent (Reply: {reply_id})")
        elif found_code:
            # Code အသစ်ဆိုရင် တင်မယ်၊ ပြီးရင် Message ID ကို မှတ်ထားမယ်
            sent_msg = await client.send_message(TARGET_CHANNEL, found_code, file=event.media)
            posted_codes[found_code] = sent_msg.id
            print(f"📌 Code Posted: {found_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    Thread(target=run_port_server, daemon=True).start()
    await client.start()
    print("🚀 Bot is live and working on single channel...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
