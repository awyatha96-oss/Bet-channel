import re
import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT FIX (Port Error မတက်အောင် အတုလုပ်ခြင်း) ---
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
SESSION_STRING = '1BZWaqwUBu54l2KPxOFDkpU-V7HDwr7Nutf7QUfvqScZTiMz_5eY3xkUu4DJLsTV-O1Jx9xxEWVy7Z4N5Q5pI8vokCMEbJSBRFRgOCB5tI4LLdS8msRAqd3X8vH5ZWGe083VuLUMx0Y5mqTG7sZoffY9uB4iJQ4HsDoeflz-V0h82KdfuycU3gnSFgfXN5VkD0oV9oIyZRzIzctMnmOHVOL6vJa6n-rE2dCDKPbtuH3Nh-1imt0ecXMo1579xBIXNY6M06CsmYuDl5rmJO1ZdsTlheYa7OnCVwch0XPEnWfrlo2psk7yYFaxSIrt4Yq0IBJ-7JG1nxxJXNw0AJNR3jz_Px4mPcR4='

SOURCE_CHANNEL = -1002609048662 
TARGET_CHANNEL = '@USDLiveMM'

def clean_content(text):
    if not text: return ""
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r't\.me/\S+', '', text)
    text = re.sub(r'@[\w\d_]+', '', text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    if event.raw_text or event.media:
        cleaned_text = clean_content(event.raw_text)
        if not cleaned_text and not event.media: return
        try:
            await client.send_message(TARGET_CHANNEL, cleaned_text, file=event.media)
            print("✅ Sent to Channel")
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    # Port Server ကို နောက်ကွယ်မှာ ပတ်ထားမယ်
    Thread(target=run_port_server, daemon=True).start()
    
    await client.start()
    print("🚀 Bot is live with Port Fix on Render!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
