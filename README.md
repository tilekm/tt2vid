# TikTok Downloader Telegram Userbot

This is a simple Telegram userbot that allows you to send video's to your friends even if you send them link to TikTok.

## Usage

1. Add the bot to a chat with you
2. Send a TikTok video link to the chat 
3. The bot will download the video and send it back as a video file

## How it works

The bot uses the [request](https://github.com/psf/requests) library to scrape the video download link from the TikTok page. It then downloads the video and uploads it to Telegram via [Pyrogram](https://github.com/pyrogram/pyrogram).

## Installation

1. `git clone https://github.com/tilekm/tt2vid.git`
2. `cd tt2vid`
3. `pip install -r requirements.txt` 
4. Obtain the API key by following Telegram’s instructions and rules at https://core.telegram.org/api/obtaining_api_id.
5. Create file `.env`
6. Write in `.env` your `API_ID` and `API_HASH` like this:   
`API_ID=YOUR_API_ID`  
`API_HASH=YOUR_API_HASH`  
7. Run `python tiktok_to_video.py`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you would like to contribute. 

Some ideas for improvements:

- Improve performance
- Improve cache system
- Add blacklist and whitelist
- Rebuild README
- Improve error handling

## License

I don't have one :(

## Author

Maulitbek Tilek