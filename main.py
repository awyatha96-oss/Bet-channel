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

db = TinyDB('/tmp/db.json')
codes_table = db.table('posted_codes')

client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    # စာသားထဲက ကြော်ငြာတွေကို ဖယ်ဖို့ event.raw_text ကိုပဲ သုံးပြီး အသစ်ပြန်ရေးမယ်
    raw_text = event.raw_text or ""
    
    # Booking Code ရှာဖွေခြင်း (စာလုံး ၄ လုံးမှ ၉ လုံး)
    codes = re.findall(r'\b[A-Z0-9]{4,9}\b', raw_text)
    found_code = codes[0] if codes else None
    
    # နိုင်တဲ့ စာလုံးများ စစ်ဆေးခြင်း
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne', 'gagné'])

    try:
        # --- Won SS (နိုင်တဲ့ပုံ) ရောက်လာလျှင် ---
        if is_won:
            # Won တဲ့အခါ Caption အဟောင်းကို မယူတော့ဘဲ "BOOM ✅" ပဲ သုံးမယ်
            new_caption = "BOOM ✅"
            
            if found_code:
                Record = Query()
                result = codes_table.get(Record.code == found_code)
                
                if result:
                    # အရင် Tip ကို Reply ထောက်ပြီး ပုံသစ်တင်မယ်
                    await client.send_message(TARGET_CH, new_caption, file=event.media, reply_to=result['msg_id'])
                else:
                    # Database ထဲမရှိရင် Reply မထောက်ဘဲ ပုံပဲတင်မယ်
                    await client.send_message(TARGET_CH, new_caption, file=event.media)
            else:
                # Code မပါရင်လည်း ပုံပဲတင်မယ်
                await client.send_message(TARGET_CH, new_caption, file=event.media)

        # --- Tip အသစ် (Booking Code) ရောက်လာလျှင် ---
        elif found_code and not is_won:
            # Tip ပေးတဲ့အခါ ကြော်ငြာစာသားတွေ အကုန်ဖယ်ပြီး Booking Code တစ်ခုတည်းပဲ Caption ထည့်မယ်
            new_tip_caption = found_code
            
            sent_msg = await client.send_message(TARGET_CH, new_tip_caption, file=event.media)
            
            # ID ကို သိမ်းမယ်
            codes_table.upsert({'code': found_code, 'msg_id': sent_msg.id}, Query().code == found_code)
            
    except Exception as e:
        print(f"❌ Error: {e}")

async def start_bot():
    await client.start()
    print("🚀 BOT IS RUNNING WITHOUT ADS!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    Thread(target=run_port_server, daemon=True).start()
    asyncio.run(start_bot())
