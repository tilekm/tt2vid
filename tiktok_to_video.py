import os

from pyrogram import Client, filters
import random
from TikTokApi import TikTokApi

did = str(random.randint(10000, 999999999))
app = Client("my_account")


def download(link):
    with TikTokApi(custom_device_id=did) as api:
        video = api.video(url=link)
        video_data = video.bytes()
        with open("out.mp4", "wb") as out_file:
            out_file.write(video_data)


@app.on_message(filters.me & (filters.chat("mengoyamen") | filters.group))
def message(client, message):
    if (not message.photo) and ("tiktok.com" in message.text):
        link = message.text
        app.delete_messages(message.chat.id, message.id)
        print("tiktok found!!")
        download(link)
        print("download completed!!")
        app.send_video(message.chat.id, "out.mp4")
        os.remove('out.mp4')


app.run()
