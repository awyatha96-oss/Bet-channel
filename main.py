import re, asyncio, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from tinydb import TinyDB, Query
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER KEEP ALIVE SERVER ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Online')

def run_port_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# --- CONFIGURATION ---
API_ID = 32646798
API_HASH = 'b989c31aea0f2408d3cfcab28f2da545'
MY_STR = '1BZWaqwUAUFhWe5a4HrhNqb1Ejrlpd9JiNOgSeqgpbnmmplFOqaVhzp2okt32gEq0j3uMXr9kXKKybh2--hyfefJmFovX2_0rqGs_G4FIUmEx341MBafKGeh0TLP0TFbX8VlgTowZzQVmqxgIRF-s_0bIR3jvyinCAhFeZjeAWdUgsRL1vWYn9owqXgjQb7aRhUHyWaUqDI0p8nyR77NodF-Ki1bCkl7_b8LOwkD28qUDGiluWBlN8dhPTl-pc_nb6nu-GE82mBO5aF_17OyRvsSNV29huVCF9V6rNHLsfjVk7THVXTpfHuMYVaXm0eGJuZTjOxqRvsTazoQNrJfeYXbCN7zyxHA='

SOURCE_CHANNELS = [-1002609048662, -1003510917243] 
TARGET_CH = '@onexbet_1xbet7'

# Database path ကို တိတိကျကျ ပေးထားပါတယ်
db = TinyDB('/tmp/db.json') 
codes_table = db.table('posted_codes')

client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    raw_text = event.raw_text or ""
    
    # ၄ လုံးကနေ ၉ လုံးအထိ Code ရှာမယ် (52CAX လိုဟာမျိုးပါအောင်)
    codes = re.findall(r'\b[A-Z0-9]{4,9}\b', raw_text)
    found_code = codes[0] if codes else None
    
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne'])

    try:
        if is_won:
            # စာသားထဲမှာ Code မပါရင် အရင်ဆုံး Database ထဲမှာ အနီးစပ်ဆုံး ရှာမယ်
            Record = Query()
            result = None
            if found_code:
                result = codes_table.get(Record.code == found_code)
            
            if result:
                await client.send_message(TARGET_CH, "BOOM ✅", file=event.media, reply_to=result['msg_id'])
            else:
                # Reply ထောက်စရာ ID ရှာမတွေ့ရင်တောင် ပုံတင်ပေးမယ်
                await client.send_message(TARGET_CH, "BOOM ✅", file=event.media)
                
        elif found_code and not is_won:
            # Code အသစ်တင်ရင် ID ကို သိမ်းမယ်
            sent_msg = await client.send_message(TARGET_CH, found_code, file=event.media)
            codes_table.upsert({'code': found_code, 'msg_id': sent_msg.id}, Record.code == found_code)
            
    except Exception as e:
        print(f"Error: {e}")

async def start_bot():
    await client.start()
    print("🚀 BOT UPDATED & RUNNING!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    Thread(target=run_port_server, daemon=True).start()
    asyncio.run(start_bot())
