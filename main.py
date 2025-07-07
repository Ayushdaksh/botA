import os
import subprocess
import requests
import tempfile

from mega import Mega
import gdown

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any supported link (YouTube, Mega, Drive, Dropbox, direct), and I’ll download it for you! 🧙‍♂️")


def download_direct(url):
    filename = url.split("/")[-1].split("?")[0]
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return filename


def download_youtube(url):
    output = "video.%(ext)s"
    cmd = ["yt-dlp", "-o", output, url]
    subprocess.run(cmd, check=True)
    for f in os.listdir():
        if f.startswith("video."):
            return f
    return None


def download_mega(url):
    mega = Mega()
    m = mega.login()
    file = m.download_url(url)
    return file


def download_gdrive(url):
    output = gdown.download(url, quiet=False)
    return output


def download_dropbox(url):
    if not url.endswith("?dl=1"):
        if "?dl=0" in url:
            url = url.replace("?dl=0", "?dl=1")
        elif "?dl=1" not in url:
            url += "?dl=1"
    return download_direct(url)


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    try:
        await update.message.reply_text("🔄 Processing your link...")
        if "youtube.com" in url or "youtu.be" in url:
            file_path = download_youtube(url)

        elif "mega.nz" in url:
            file_path = download_mega(url)

        elif "drive.google.com" in url:
            file_path = download_gdrive(url)

        elif "dropbox.com" in url:
            file_path = download_dropbox(url)

        elif url.startswith("http"):
            file_path = download_direct(url)

        else:
            await update.message.reply_text("⚠️ Unsupported link.")
            return

        if not file_path or not os.path.exists(file_path):
            await update.message.reply_text("❌ Failed to download the file.")
            return

        await update.message.reply_document(document=open(file_path, "rb"))
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    app = ApplicationBuilder().token("7773436335:AAHilsR97qEEIQMJIFOWX_dJQM0Hu750sw8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("🚀 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
