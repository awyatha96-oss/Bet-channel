import re
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION ---
API_ID = 32153130
API_HASH = '66168465c6360e3d856a8a53a3d21e84'
SESSION_STRING = '1BZWaqwUBu54l2KPxOFDkpU-V7HDwr7Nutf7QUfvqScZTiMz_5eY3xkUu4DJLsTV-O1Jx9xxEWVy7Z4N5Q5pI8vokCMEbJSBRFRgOCB5tI4LLdS8msRAqd3X8vH5ZWGe083VuLUMx0Y5mqTG7sZoffY9uB4iJQ4HsDoeflz-V0h82KdfuycU3gnSFgfXN5VkD0oV9oIyZRzIzctMnmOHVOL6vJa6n-rE2dCDKPbtuH3Nh-1imt0ecXMo1579xBIXNY6M06CsmYuDl5rmJO1ZdsTlheYa7OnCVwch0XPEnWfrlo2psk7yYFaxSIrt4Yq0IBJ-7JG1nxxJXNw0AJNR3jz_Px4mPcR4='

SOURCE_CHANNEL = -1002609048662 
TARGET_CHANNEL = '@onexbet_1xbet7'

def clean_content(text):
    if not text:
        return ""
    
    # ၁။ Website Link တွေ အကုန်ဖျက်မယ် (http, https, t.me link များ)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r't\.me/\S+', '', text)
    
    # ၂။ Telegram Username (@...) တွေ အကုန်ဖျက်မယ်
    text = re.sub(r'@[\w\d_]+', '', text)
    
    # ၃။ လိုအပ်တဲ့ စာသား (Betting Code, Odds, စတာတွေ) ပဲ ကျန်အောင် Space အပိုတွေ ဖြတ်မယ်
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    # စာသား သို့မဟုတ် ပုံ ပါမှ အလုပ်လုပ်မယ်
    if event.raw_text or event.media:
        cleaned_text = clean_content(event.raw_text)
        
        # အကယ်၍ စာသားက Link တွေချည်းပဲဖြစ်နေလို့ အကုန်ပြောင်သွားရင် ဘာမှမပို့ဘူး
        if not cleaned_text and not event.media:
            return

        try:
            # client.send_message ကို သုံးထားလို့ "Forwarded from" မပါပါဘူး
            # file=event.media က ပုံကို မူရင်းအတိုင်း ပို့ပေးမှာပါ
            await client.send_message(
                TARGET_CHANNEL, 
                cleaned_text, 
                file=event.media
            )
            print("✅ ပို့ပြီးပါပြီ (Link/Username များ ဖယ်ရှားပြီး)")
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    await client.start()
    print("🚀 Bot စတင်အလုပ်လုပ်နေပါပြီ... (Link Filter အသင့်ဖြစ်ပါပြီ)")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
