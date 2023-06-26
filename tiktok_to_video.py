import os
import asyncio
from pyrogram import Client, filters
import random
from TikTokApi import TikTokApi
from pyrogram.errors import FloodWait

from pyrogram.types import ChatPermissions

import time
from time import sleep
import random
did = str(random.randint(10000, 999999999))
api = TikTokApi(custom_device_id=did)
app = Client("my_account", api_id=21157952, api_hash='c0bd5296069e9160fbbada61734d4afa')


# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""  # to be printed
    typing_symbol = "▒"

    while (tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.05)  # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.02)

        except FloodWait as e:
            sleep(e.x)


@app.on_message(filters.me & (filters.chat("mengoyamen") | filters.group))
async def message(client, message):
    if (not message.photo) and ("tiktok.com" in message.text):
        link = message.text
        print("tiktok found!!")
        with TikTokApi(custom_device_id=did) as api:
            video = api.video(url=link)
            if video.info_full()['itemInfo']['itemStruct']['video']['duration']:
                await app.delete_messages(message.chat.id, message.id)
                video_data = video.bytes()
                with open("out.mp4", "wb") as out_file:
                    out_file.write(video_data)
                print("download completed!!")
                await app.send_video(message.chat.id, "out.mp4")
                os.remove('out.mp4')
            else:
                print('Image Found!!')


app.run()
