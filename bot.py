import re
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8627945459:AAGftfwkj0vK6gd6thzUVGUJqvxFqei130U"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot running")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.run_polling()
