import re, asyncio, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from tinydb import TinyDB, Query
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT FIX (Render မပိတ်သွားအောင် လုပ်ပေးတာပါ) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Running')

def run_port_server():
    # Render ကပေးတဲ့ PORT ကိုသုံးပါမယ်၊ မရှိရင် 8080 ကိုသုံးပါမယ်
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"🌍 Web Server started on port {port}")
    server.serve_forever()

# --- CONFIGURATION ---
API_ID = 32646798
API_HASH = 'b989c31aea0f2408d3cfcab28f2da545'
MY_STR = '1BZWaqwUAUFhWe5a4HrhNqb1Ejrlpd9JiNOgSeqgpbnmmplFOqaVhzp2okt32gEq0j3uMXr9kXKKybh2--hyfefJmFovX2_0rqGs_G4FIUmEx341MBafKGeh0TLP0TFbX8VlgTowZzQVmqxgIRF-s_0bIR3jvyinCAhFeZjeAWdUgsRL1vWYn9owqXgjQb7aRhUHyWaUqDI0p8nyR77NodF-Ki1bCkl7_b8LOwkD28qUDGiluWBlN8dhPTl-pc_nb6nu-GE82mBO5aF_17OyRvsSNV29huVCF9V6rNHLsfjVk7THVXTpfHuMYVaXm0eGJuZTjOxqRvsTazoQNrJfeYXbCN7zyxHA='

SOURCE_CHANNELS = [-1002609048662, -1003510917243] 
TARGET_CH = '@onexbet_1xbet7'

db = TinyDB('db.json')
codes_table = db.table('posted_codes')

client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    raw_text = event.raw_text or ""
    codes = re.findall(r'\b[A-Z0-9]{5,9}\b', raw_text)
    found_code = codes[0] if codes else None
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne'])

    try:
        if is_won and found_code:
            Record = Query()
            result = codes_table.get(Record.code == found_code)
            if result:
                await client.send_message(TARGET_CH, "BOOM ✅", file=event.media, reply_to=result['msg_id'])
        elif found_code and not is_won:
            sent_msg = await client.send_message(TARGET_CH, found_code, file=event.media)
            codes_table.insert({'code': found_code, 'msg_id': sent_msg.id})
    except Exception: pass

async def start_bot():
    await client.start()
    print("🚀 BOT IS LIVE AND PORT IS BOUND!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Web Server ကို Background မှာ Run ပါမယ်
    Thread(target=run_port_server, daemon=True).start()
    
    # Bot ကို Run ပါမယ်
    asyncio.run(start_bot())
