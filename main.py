from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from mega import Mega
import os

# Mega login (anonymous)
mega = Mega()
m = mega.login()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /getmega <mega_link> to download")

async def get_mega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /getmega <mega_link>")
        return
    
    mega_link = context.args[0]
    try:
        file = m.download_url(mega_link, dest_filename="mega_temp_file")
        file_name = os.path.basename(file)
        await update.message.reply_document(document=open(file, 'rb'), filename=file_name)
        os.remove(file)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7773436335:AAHilsR97qEEIQMJIFOWX_dJQM0Hu750sw8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getmega", get_mega))
    print("Bot running...")
    app.run_polling()
