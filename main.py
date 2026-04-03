import re
import asyncio
import os
import base64
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

# String ကို ပြန်ပြင်ပေးမည့်အပိုင်း
RAW_STRING = '1BZWaqwUBu54l2KPxOFDkpU-V7HDwr7Nutf7QUfvqScZTiMz_5eY3xkUu4DJLsTV-O1Jx9xxEWVy7Z4N5Q5pI8vokCMEbJSBRFRgOCB5tI4LLdS8msRAqd3X8vH5ZWGe083VuLUMx0Y5mqTG7sZoffY9uB4iJQ4HsDoeflz-V0h82KdfuycU3gnSFgfXN5VkD0oV9oIyZRzIzctMnmOHVOL6vJa6n-rE2dCDKPbtuH3Nh-1imt0ecXMo1579xBIXNY6M06CsmYuDl5rmJO1ZdsTlheYa7OnCVwch0XPEnWfrlo2psk7yYFaxSIrt4Yq0IBJ-7JG1nxxJXNw0AJNR3jz_Px4mPcR4='

def fix_padding(s):
    s = s.strip()
    return s + '=' * (-len(s) % 4)

SESSION_STRING = fix_padding(RAW_STRING)

SOURCE_CHANNEL = -1002609048662 
TARGET_CHANNEL = '@onexbet_1xbet7'

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
        elif found_code:
            sent_msg = await client.send_message(TARGET_CHANNEL, found_code, file=event.media)
            posted_codes[found_code] = sent_msg.id
    except Exception as e:
        print(f"Error: {e}")

async def main():
    Thread(target=run_port_server, daemon=True).start()
    try:
        await client.start()
        print("Bot is started successfully!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
