import os
from functools import lru_cache

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from time import sleep
import requests

load_dotenv()
app = Client("my_account", api_id=os.getenv('API_ID'), api_hash=os.getenv('API_HASH'))

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}


# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def typing(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""  # to be printed
    typing_symbol = "▒"

    while tbp != orig_text:
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.05)  # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.02)

        except FloodWait as e:
            sleep(e)


@lru_cache(5)
def download_video(url):
    response = requests.get(url, headers=headers)
    spl = response.url.split('/')
    if spl[4] == 'video':
        video_id = spl[5].split('?')[0]
        request_url = f'https://www.tikwm.com/video/media/play/${video_id}.mp4'
        response = requests.get(request_url, headers=headers)
        video_link = response.url
        return video_link
    else:
        return False


@app.on_message(filters.me & (filters.private | filters.group))
async def tt2vid(_, message):
    tt_link = message.text
    if tt_link and ("tiktok.com" in tt_link):
        link = download_video(tt_link)
        if link:
            await app.delete_messages(message.chat.id, message.id)
            await app.send_video(message.chat.id, link, disable_notification=True)
            print('Video Sent!!')
        else:
            print('Image Found!!')


print('App is Started!!!')
app.run()
