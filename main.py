import re
import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT FIX (Render မသေသွားအောင် လုပ်ပေးတာပါ) ---
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

# Render Environment ထဲက SESSION ကို လှမ်းယူပါတယ်
SESSION_STRING = os.environ.get("SESSION")

SOURCE_CHANNELS = [-1002609048662, -1003510917243] 
TARGET_CHANNEL = '@onexbet_1xbet7'

posted_codes = {}

# --- BOT CLIENT ---
client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    global posted_codes
    if not event.media: return

    raw_text = event.raw_text
    
    # Booking Code ထုတ်ယူခြင်း
    clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')
    codes = re.findall(r'\b[A-Z0-9]{5,8}\b', clean_text)
    found_code = codes[0] if codes else None
    
    # နိုင်တဲ့ပုံ (Won SS) ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne'])

    try:
        if is_won:
            # နိုင်တဲ့ပုံဆိုရင် Code တူတဲ့ Post ကို Reply ထောက်မယ်
            reply_id = posted_codes.get(found_code) if found_code else None
            await client.send_message(TARGET_CHANNEL, "BOOM ✅", file=event.media, reply_to=reply_id)
        elif found_code:
            # Code အသစ်ဆိုရင် တင်မယ်၊ ပြီးရင် Message ID ကို မှတ်ထားမယ်
            sent_msg = await client.send_message(TARGET_CHANNEL, found_code, file=event.media)
            posted_codes[found_code] = sent_msg.id
    except Exception as e:
        print(f"Error occurred: {e}")

async def start_bot():
    # Environment Variable က String ကို သုံးပြီး Bot စတင်ပါမယ်
    try:
        await client.start()
        print("🚀 BOT IS SUCCESSFULLY ONLINE!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == '__main__':
    # Web Server အတွက် Thread ဖွင့်ခြင်း
    Thread(target=run_port_server, daemon=True).start()
    
    # Bot စတင်ခြင်း
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())
