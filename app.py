# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from flask import Flask, request, render_template
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Load bot token from Render environment variables
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN)

app = Flask(__name__)

# Build telegram application
telegram_app = Application.builder().token(TOKEN).build()

# ---------- BOT COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working! Webhook active 🚀")


telegram_app.add_handler(CommandHandler("start", start))


# ---------- FLASK ROUTES ----------
@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot)
    telegram_app.process_update(update)
    return "OK", 200


# ---------- RUN APP ----------
if __name__ == "__main__":
    telegram_app.initialize()  # Required for PTB v20 webhook mode

    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)


