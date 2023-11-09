from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from time import sleep
import requests
import urllib.request
from bs4 import BeautifulSoup
from functools import lru_cache


app = Client("my_account")
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


@lru_cache(maxsize=7)
def download_video(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('link', {'rel': 'canonical'}).attrs['href']
    video_id = link.split('/')[-1:][0]
    request_url = f'https://api.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'
    response = requests.get(request_url, headers=headers)
    try:
        video_link = response.json()['aweme_list'][0]['video']['play_addr']['url_list'][2]
        urllib.request.urlretrieve(video_link, 'out.mp4')
        return 'out.mp4'
    except IndexError:
        return False


@app.on_message(filters.me & (filters.private | filters.group))
async def tt2vid(_, message):
    tt_link = message.text
    if tt_link and ("tiktok.com" in tt_link):
        file_path = download_video(tt_link)
        if file_path:
            await app.delete_messages(message.chat.id, message.id)
            await app.send_video(message.chat.id, file_path)
            print('Video Sent!!')
        else:
            print('Image Found!!')


print('App is Started!!!')
app.run()
