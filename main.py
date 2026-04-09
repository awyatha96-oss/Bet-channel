import re, asyncio, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from tinydb import TinyDB, Query
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT KEEP ALIVE ---
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

# Database Setup
db = TinyDB('/tmp/db.json')
codes_table = db.table('posted_codes')

client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    # စာသားသက်သက်လာရင် လုံးဝမယူဘူး
    if not event.media:
        return 

    raw_text = event.raw_text or ""
    
    # ၁။ Booking Code ရှာဖွေခြင်း (စာလုံး ၄ လုံးမှ ၉ လုံး)
    booking_codes = re.findall(r'\b[A-Z0-9]{4,9}\b', raw_text)
    
    # ၂။ Additional Info ဂဏန်း ၃ လုံး ရှာဖွေခြင်း (ပုံထဲက 428 လိုဟာမျိုး)
    info_numbers = re.findall(r'\b\d{3}\b', raw_text)
    
    # နိုင်တဲ့စာသား စစ်ဆေးခြင်း
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom', 'paye', 'gagne', 'gagné'])

    try:
        # --- Won SS (နိုင်တဲ့ပုံ) ရောက်လာလျှင် ---
        if is_won:
            # Won တဲ့အခါ တခြားစာသားတွေအကုန်ဖြုတ်ပြီး BOOM ✅ ပဲ သုံးမယ်
            new_caption = "BOOM ✅"
            
            # Additional Info နံပါတ်တူတာရှိမရှိ Database မှာ အရင်စစ်မယ်
            target_id = None
            if info_numbers:
                Record = Query()
                # အခု Won SS ထဲမှာပါတဲ့ ဂဏန်း ၃ လုံးနဲ့ အရင်တင်ထားတဲ့ Tip ထဲက ဂဏန်းနဲ့ တိုက်စစ်မယ်
                result = codes_table.get(Record.info_num == info_numbers[0])
                if result:
                    target_id = result['msg_id']
            
            # နံပါတ်ကိုက်ညီရင် Reply ထောက်မယ်၊ မကိုက်ရင် ပုံပဲတင်မယ်
            if target_id:
                await client.send_message(TARGET_CH, new_caption, file=event.media, reply_to=target_id)
            else:
                await client.send_message(TARGET_CH, new_caption, file=event.media)

        # --- Tip အသစ် (Booking Code) ရောက်လာလျှင် ---
        elif booking_codes and not is_won:
            # တခြားစာသားတွေဖြုတ်ပြီး Booking Code တစ်ခုတည်းပဲ Caption ထည့်မယ်
            found_booking = booking_codes[0]
            found_info = info_numbers[0] if info_numbers else "None"
            
            sent_msg = await client.send_message(TARGET_CH, found_booking, file=event.media)
            
            # Booking Code နဲ့ Additional Info နံပါတ်ကိုပါ တွဲသိမ်းမယ်
            codes_table.upsert({
                'code': found_booking, 
                'info_num': found_info, 
                'msg_id': sent_msg.id
            }, Query().code == found_booking)
            
    except Exception as e:
        print(f"Error: {e}")

async def start_bot():
    await client.start()
    print("🚀 BOT IS RUNNING: TRACKING ADDITIONAL INFO NUMBERS!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    Thread(target=run_port_server, daemon=True).start()
    asyncio.run(start_bot())
