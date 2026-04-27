import os
import asyncio
import yt_dlp
import traceback
from telethon import TelegramClient
from telethon.sessions import StringSession
from deep_translator import GoogleTranslator

# ኮንፊገሬሽን
try:
    API_ID = int(os.environ.get('API_ID'))
    API_HASH = os.environ.get('API_HASH')
    SESSION_STR = os.environ.get('SESSION_STRING')
except Exception as e:
    print(f"የመለያ ስህተት (Secrets Error): {e}")

YOUTUBE_CH_URL = 'https://www.youtube.com/@LiveNOWfromFOX/videos' 
TELEGRAM_CH_NAME = '@InfoMela06' 
MY_AD_MESSAGE = "\n📢 የቴሌግራም ቦት እና አውቶሜሽን ስራዎችን እንሰራለን። 👉 ለማነጋገር: @ያንተ_ዩዘር_ኔም"

def download_latest_video():
    print("ቪዲዮ በመፈለግ ላይ...")
    ydl_opts = {
        'outtmpl': 'bot_video.mp4',
        'format': 'mp4',
        'playlist_items': '1', 
        'max_filesize': 40000000,
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(YOUTUBE_CH_URL, download=True)
        raw_title = info['entries'][0]['title']
        translated = GoogleTranslator(source='auto', target='am').translate(raw_title)
        return translated, 'bot_video.mp4'

async def main():
    try:
        title, file_path = download_latest_video()
        print(f"ቪዲዮው ወርዷል: {title}")
        
        client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)
        await client.start()
        
        print("ወደ ቴሌግራም በመጫን ላይ...")
        await client.send_file(TELEGRAM_CH_NAME, file_path, caption=f"🎬 **{title}**\n{MY_AD_MESSAGE}")
        await client.disconnect()
        print("በተሳካ ሁኔታ ተጠናቋል!")
        
    except Exception as e:
        print("!!! ስህተት ተከስቷል !!!")
        print(traceback.format_exc()) # ሙሉውን ስህተት እንዲያሳይ

if __name__ == '__main__':
    asyncio.run(main())
