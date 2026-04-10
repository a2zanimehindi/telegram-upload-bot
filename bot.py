import re
import requests
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes



BOT_TOKEN = os.getenv("8627945459:AAGftfwkj0vK6gd6thzUVGUJqvxFqei130U")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")
VIDARA_API = os.getenv("95a2f013c6166662a507cc3b737cbdd1198f50dec5199c80b195439a9bbc98d6")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

queue = asyncio.Queue()

def extract_drive_id(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None

def upload_to_vidara(url, title):
    headers = {"Authorization": f"Bearer {VIDARA_API}"}
    data = {"url": url, "title": title}
    r = requests.post("https://vidara.so/api/upload/url", json=data, headers=headers)
    return r.text

async def worker(app):
    while True:
        update, link, title = await queue.get()
        try:
            msg = await update.message.reply_text("⬆️ Uploading...")
            result = upload_to_vidara(link, title)
            await msg.edit_text("✅ Done")
            await update.message.reply_text(result)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
        queue.task_done()

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text

    if "drive.google.com" in text:
        file_id = extract_drive_id(text)
        if file_id:
            direct = f"https://drive.google.com/uc?export=download&id={file_id}"
            await queue.put((update, direct, "Drive Upload"))
            await update.message.reply_text("📥 Added to queue")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    # start worker
    asyncio.create_task(worker(app))

    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
