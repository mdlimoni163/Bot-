from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8204385402:AAFVVmaMDPPCMGGDH2lrsDAD6kzowy4yvXs"
ADMIN_ID = 7679648228  # replace with your Telegram user ID

stored_files = []  # use database in production

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not stored_files:
        await update.message.reply_text("No files available yet.")
        return

    await update.message.reply_text("Sending available files...")
    for file_id in stored_files:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file_id
        )

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not allowed to upload files.")
        return

    document = update.message.document
    stored_files.append(document.file_id)
    await update.message.reply_text("File saved successfully.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, save_file))

app.run_polling()
