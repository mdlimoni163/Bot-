from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# ================= CONFIG =================
BOT_TOKEN = "8204385402:AAFVVmaMDPPCMGGDH2lrsDAD6kzowy4yvXs"
ADMIN_ID = 7679648228  # your Telegram numeric ID
# ==========================================

# Temporary storage (use DB in production)
stored_videos = []


# /start → send all saved videos to user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not stored_videos:
        await update.message.reply_text("No videos available.")
        return

    for item in stored_videos:
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=item["file_id"],
            caption=item["caption"]
        )


# /import → reply to a forwarded video to save it
async def import_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not allowed to use this command.")
        return

    reply = update.message.reply_to_message

    if not reply or not reply.video:
        await update.message.reply_text(
            "Reply to a VIDEO message with /import."
        )
        return

    file_id = reply.video.file_id
    caption = reply.caption or "Episode"

    # prevent duplicates
    for v in stored_videos:
        if v["file_id"] == file_id:
            await update.message.reply_text("This video is already imported.")
            return

    stored_videos.append({
        "file_id": file_id,
        "caption": caption
    })

    await update.message.reply_text("Video imported successfully.")


# ================= RUN BOT =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("import", import_video))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
