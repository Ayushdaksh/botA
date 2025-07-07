import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from mega import Mega

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /getmega <link> to download from MEGA.")

async def getmega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /getmega <mega_link>")
        return

    mega_link = context.args[0]
    await update.message.reply_text("📥 Downloading from MEGA...")

    try:
        mega = Mega()
        m = mega.login()
        file = m.download_url(mega_link, dest_path="/tmp/")
        file_name = os.path.basename(file)

        await update.message.reply_document(open(file, "rb"), filename=file_name)
        os.remove(file)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7773436335:AAHilsR97qEEIQMJIFOWX_dJQM0Hu750sw8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getmega", getmega))
    print("Bot is running...")
    app.run_polling()
