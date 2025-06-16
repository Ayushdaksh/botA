# bot_a.py
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_B_USERNAME = "bot4261_bot"  # Without @

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file_id = None

    # Check for video or photo
    if message.video:
        file_id = message.video.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id  # highest resolution

    if file_id:
        bot_b_link = f"https://t.me/{BOT_B_USERNAME}?start={file_id}"
        await message.reply_text(f"🔗 Here’s your link: {bot_b_link}")
    else:
        await message.reply_text("❌ Send me a photo or video, buddy!")

app = ApplicationBuilder().token("7961258145:AAFXV1gTvFv8zyomJwzU_iBou9r3DtXq9q0").build()
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
app.run_polling()
