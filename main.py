import re
import random
import requests
from telethon import TelegramClient, events

# --- CONFIGURATION ---
API_ID = 32153130
API_HASH = '66168465c6360e3d856a8a53a3d21e84'

# Target Source Channels
SOURCE_CHANNELS = [-1002609048662, -1001587577908, -1001545992843]

# Your Channel
TARGET_CHANNEL = '@onexbet_1xbet7'

# Your Channel Links
MY_LINKS = [
    'https://t.me/+zNJIrwnwpzs2ZmJl',
    'https://t.me/+IzGmAIbAPu81N2Rl'
]

# Words to filter out
BLACKLIST = ['1xbet', 'melbet', 'promocode', 'bonus', 'register', 'deposit', 'betting']

def translate_to_english(text):
    try:
        if not text.strip():
            return text
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fr&tl=en&dt=t&q={text}"
        response = requests.get(url, timeout=10)
        translated_parts = [part[0] for part in response.json()[0] if part[0]]
        return "".join(translated_parts)
    except:
        return text

def clean_and_process(text):
    # 1. Translate French to English
    translated_text = translate_to_english(text)
    
    # 2. Filter lines and Replace links
    lines = translated_text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if not any(word in line.lower() for word in BLACKLIST):
            url_pattern = r'https?://\S+|@[\w\d_]+'
            processed_line = re.sub(url_pattern, lambda x: random.choice(MY_LINKS), line)
            cleaned_lines.append(processed_line)
    
    return '\n'.join(cleaned_lines)

client = TelegramClient('usd_live_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def my_event_handler(event):
    if event.raw_text:
        final_text = clean_and_process(event.raw_text)
        
        if final_text.strip():
            try:
                await client.send_message(TARGET_CHANNEL, final_text, file=event.media)
                print(f"Done: {event.chat_id}")
            except Exception as e:
                print(f"Error: {e}")

print("Bot is running...")
client.start()
client.run_until_disconnected()
