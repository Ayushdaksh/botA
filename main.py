# bot_a.py
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_B_USERNAME = "bot4261_bot"

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    bot = context.bot

    if message.video:
        file = await bot.get_file(message.video.file_id)
    elif message.photo:
        file = await bot.get_file(message.photo[-1].file_id)
    else:
        await message.reply_text("Send a video or image.")
        return
    await update.message.reply_text(
    "Click to view media: [▶️ View in Bot B](https://t.me/YourBotBUsername?start={file_path})\n\n"
    "📌 Make sure you've clicked 'Start' in Bot B at least once!",
    parse_mode="Markdown"
)
    

    # This is the direct link to the file
    file_path = file.file_path
    await message.reply_text(f"https://t.me/{BOT_B_USERNAME}?start={file_path}")

app = ApplicationBuilder().token("7961258145:AAFXV1gTvFv8zyomJwzU_iBou9r3DtXq9q0").build()
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
app.run_polling()
