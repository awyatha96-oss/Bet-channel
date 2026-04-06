import re, asyncio, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION ---
API_ID = 32153130
API_HASH = '66168465c6360e3d856a8a53a3d21e84'

# !!! ဒီနေရာမှာ သင့် String ကို ' ' ကြားထဲ အသေထည့်ပါ !!!
MY_STR = '1BZWaqwUBu8D6AbOSX-7BpStNCyYD0yj_VYik53V2wssviWILbg-0OgNND3FOGog2XwXKtALIoIRoWwGFfr3I8tST-w9svHxDHWwkpk6CxVtN_csivY_HsTXQawvBDPrZqFbXUeQgvt4fN3Eb2Ndj156J-c0CJPN7UgTgw9Dhbc_Hqxby4weu8rDaicRqZ94muLUDPXzo9ku66OGfPBSutm6XgKIfqjTg2Djb-njaSuuADqQPq5-5lz3eoHCpP0VK8Vp8yDEGwHw5VVH-yZXV4yO3u5xzhdVJtCtR2fxIsMondvmwid_no4XWWy6YeBDDQcRaeQj_UcMFQTTOjc3iZZxjbIbdz5U='

SOURCE_CHANNELS = [-1002609048662, -1003510917243] 
TARGET_CH = '@onexbet_1xbet7'

posted_codes = {}

# Client ကို တိုက်ရိုက် တည်ဆောက်ပါတယ်
client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    global posted_codes
    if not event.media: return
    
    raw_text = event.raw_text
    clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')
    codes = re.findall(r'\b[A-Z0-9]{5,8}\b', clean_text)
    found_code = codes[0] if codes else None
    is_won = any(x in raw_text.lower() for x in ['paid out', 'won', 'success', 'boom'])

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
    # Login တောင်းတဲ့ ပြဿနာကို ကျော်ဖို့ connect နဲ့ start ကို ခွဲသုံးပါမယ်
    await client.connect()
    if not await client.is_user_authorized():
        # String မှားနေရင် Log ထဲမှာ ဒါကို ပြပါလိမ့်မယ်
        print("❌❌ ERROR: SESSION STRING IS INVALID OR EXPIRED ❌❌")
        return
    
    print("🚀🚀 BOT IS SUCCESSFULLY ONLINE! 🚀🚀")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Render အတွက် Port မလိုတဲ့ ရိုးရိုးပုံစံနဲ့ပဲ အရင်စမ်းပါမယ်
    asyncio.run(start_bot())
