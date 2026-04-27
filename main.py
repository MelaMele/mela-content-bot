# 2. ከዚያ በኋላ ዋናውን ስክሪፕት ማስጀመር
import os
import asyncio
import yt_dlp
import time
from telethon import TelegramClient
from deep_translator import GoogleTranslator

# --- ኮንፊገሬሽን ---
YOUTUBE_CH_URL = 'https://www.youtube.com/@LiveNOWfromFOX/videos'
TELEGRAM_CH_NAME = '@InfoMela06'

api_id = 37587100
api_hash = '79e0f261b3c2dae2b3c14bbb5bedf9d0'

MY_AD_MESSAGE = """
📢 **የማስታወቂያ አገልግሎት**
የእርስዎን ምርት ወይም አገልግሎት በዚህ ቻናል ላይ ማስተዋወቅ ይፈልጋሉ?
ፈጣን እና አስተማማኝ የቴሌግራም ቦቶችን እና አውቶሜሽን ስራዎችን እንሰራለን።
👉 ለማነጋገር: @ያንተ_ዩዘር_ኔም
"""

def download_latest_video():
    ydl_opts = {
        'outtmpl': 'bot_video.mp4',
        'format': 'mp4',
        'playlist_items': '1',
        'max_filesize': 45000000,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(YOUTUBE_CH_URL, download=True)
        raw_title = info['entries'][0]['title']
        translated_title = GoogleTranslator(source='auto', target='am').translate(raw_title)
        return translated_title, 'bot_video.mp4'

async def upload_to_telegram(title, file_path):
    client = TelegramClient('business_session', api_id, api_hash)
    await client.start()
    full_caption = f"🎬 **{title}**\n\n{MY_AD_MESSAGE}"
    await client.send_file(TELEGRAM_CH_NAME, file_path, caption=full_caption)
    await client.disconnect()
    if os.path.exists(file_path):
        os.remove(file_path)

async def run_forever():
    print("🚀 የገቢ ማሽኑ ስራ ጀምሯል...")
    while True:
        try:
            title, file_path = download_latest_video()
            await upload_to_telegram(title, file_path)
            print(f"✅ ተሳክቷል! ቀጣዩ ፍተሻ ከ 1 ሰዓት በኋላ ይሆናል።")
        except Exception as e:
            print(f"ስህተት ተፈጥሯል: {e}")
        await asyncio.sleep(3600)

await run_forever()
