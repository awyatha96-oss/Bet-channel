import re, asyncio, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION (Website မှာ သုံးခဲ့တဲ့ အသစ်တွေပါ) ---
API_ID = 32646798
API_HASH = 'b989c31aea0f2408d3cfcab28f2da545'

# သင်အခုပေးလိုက်တဲ့ String အသစ်
MY_STR = '1BZWaqwUAUFhWe5a4HrhNqb1Ejrlpd9JiNOgSeqgpbnmmplFOqaVhzp2okt32gEq0j3uMXr9kXKKybh2--hyfefJmFovX2_0rqGs_G4FIUmEx341MBafKGeh0TLP0TFbX8VlgTowZzQVmqxgIRF-s_0bIR3jvyinCAhFeZjeAWdUgsRL1vWYn9owqXgjQb7aRhUHyWaUqDI0p8nyR77NodF-Ki1bCkl7_b8LOwkD28qUDGiluWBlN8dhPTl-pc_nb6nu-GE82mBO5aF_17OyRvsSNV29huVCF9V6rNHLsfjVk7THVXTpfHuMYVaXm0eGJuZTjOxqRvsTazoQNrJfeYXbCN7zyxHA='

SOURCE_CHANNELS = [-1002609048662, -1003510917243] 
TARGET_CH = '@onexbet_1xbet7'

posted_codes = {}
client = TelegramClient(StringSession(MY_STR.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    global posted_codes
    if not event.media: return
    
    raw_text = event.raw_text or ""
    # Booking Code ရှာဖွေခြင်း
    clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')
    codes = re.findall(r'\b[A-Z0-9]{5,8}\b', clean_text)
    found_code = codes[0] if codes else None
    
    # နိုင်တဲ့ပုံ (Success/Won) စစ်ဆေးခြင်း
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
    try:
        await client.start()
        print("🚀🚀 BOT IS SUCCESSFULLY ONLINE AND RUNNING! 🚀🚀")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"❌ LOGIN ERROR: {e}")

if __name__ == '__main__':
    # Render အတွက် Port မလိုတဲ့ ရိုးရိုးပုံစံနဲ့ အရင် Run ပါမယ်
    asyncio.run(start_bot())
