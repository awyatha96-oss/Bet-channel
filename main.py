import re, asyncio, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT FIX ---
def run_port_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), BaseHTTPRequestHandler)
    server.serve_forever()

# --- CONFIGURATION ---
API_ID = 32153130
API_HASH = '66168465c6360e3d856a8a53a3d21e84'
MY_STR = '1BZWaqwUBu8D6AbOSX-7BpStNCyYD0yj_VYik53V2wssviWILbg-0OgNND3FOGog2XwXKtALIoIRoWwGFfr3I8tST-w9svHxDHWwkpk6CxVtN_csivY_HsTXQawvBDPrZqFbXUeQgvt4fN3Eb2Ndj156J-c0CJPN7UgTgw9Dhbc_Hqxby4weu8rDaicRqZ94muLUDPXzo9ku66OGfPBSutm6XgKIfqjTg2Djb-njaSuuADqQPq5-5lz3eoHCpP0VK8Vp8yDEGwHw5VVH-yZXV4yO3u5xzhdVJtCtR2fxIsMondvmwid_no4XWWy6YeBDDQcRaeQj_UcMFQTTOjc3iZZxjbIbdz5U='

# --- SOURCE CHANNELS (ဒီနေရာမှာ Channel နှစ်ခုလုံး ထည့်ထားပါတယ်) ---
SOURCE_CHANNELS = [-1002609048662, -1003510917243] 

TARGET_CH = '@onexbet_1xbet7'

posted_codes = {}

client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

# handler မှာ chats=SOURCE_CHANNELS လို့ ပြောင်းလိုက်ပါတယ်
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
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
    await client.start()
    print("🚀 BOT IS SUCCESSFULLY ONLINE WITH 2 SOURCE CHANNELS!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    Thread(target=run_port_server, daemon=True).start()
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"Startup Error: {e}")
