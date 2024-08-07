import os
import subprocess
from functools import lru_cache
from time import sleep

import requests
from PIL import Image
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

load_dotenv()
app = Client("my_account", api_id=os.getenv('API_ID'), api_hash=os.getenv('API_HASH'))

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}
api = "https://www.tikwm.com/api/"


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


def get_max_dimensions(images):
    max_width = 0
    max_height = 0
    for img in range(images):
        with Image.open("images/image" + str(img) + ".jpg") as i:
            width, height = i.size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height
    return max_width, max_height


@lru_cache(1)
def download_video(url):
    response = requests.get(api, headers=headers, params={'url': url})
    data = response.json()
    if data.get('code') == -1:
        return None
    if data["data"]["duration"] > 0:
        return data["data"]["play"]
    else:
        images = data["data"]["images"]
        length = len(images)
        if not os.path.exists("images"):
            os.mkdir("images")
        for i in range(length):
            r = requests.get(images[i], headers=headers)
            with open(f"images/image{i}.jpg", "wb") as f:
                f.write(r.content)
        with open("output.mp3", "wb") as f:
            f.write(requests.get(data["data"]["play"], headers=headers).content)
        audio_file = "output.mp3"
        output_file = "output.mp4"
        image_duration = 3
        max_width, max_height = get_max_dimensions(length)

        result = ['ffmpeg', '-y', '-threads', '1']
        filter_complex = ""
        concat_inputs = ""

        for i in range(length):
            result += ['-loop', '1', '-t', str(image_duration), '-i', f'images/image{i}.jpg']
            filter_complex += (f"[{i}:v]fps=1,scale={max_width - 1}:{max_height - 1}:force_original_aspect_ratio"
                               f"=decrease,setsar=sar=1/1,pad={max_width}:{max_height}:(ow-iw)/2:(oh-ih)/2,"
                               f"format=yuvj420p[image{i}];")
            concat_inputs += f"[image{i}]"

        filter_complex += f"{concat_inputs}concat=n={length}:v=1:a=0[outv]"
        result += [
            '-i', audio_file,
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-map', f'{length}:a',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            '-movflags', 'faststart',
            '-preset', 'fast',
            '-crf', '18'
        ]
        result += [output_file, '-async', '1']

        subprocess.run(result)

        return output_file


@app.on_message(filters.me & (filters.private | filters.group))
async def tt2vid(_, message):
    tt_link = message.text
    if tt_link and ("tiktok.com" in tt_link):
        await app.delete_messages(message.chat.id, message.id)
        link = download_video(tt_link)
        if link:
            await app.send_video(message.chat.id, link, disable_notification=True)
            print('Video Sent!!')
        else:
            print('Error!!')


print('App is Started!!!')
app.run()
