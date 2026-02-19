import json
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from nintendo_search import search_nintendo_id
from add_games import load_watchlist, WATCH_FILE
from notifier import TOKEN

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /add <game name>")
        return
    query = " ".join(context.args)
    results = search_nintendo_id(query)
    if not results:
        await update.message.reply_text("No results found - check spelling.")
        return
    response = "Pick a game:\n"
    for i, game in enumerate(results):
        response += f"{i+1}. {game['title']} (nsuid: {game['nsuid']})\n"
    context.user_data["results"] = results
    await update.message.reply_text(response)

async def pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = context.user_data.get("results")
    if not results:
        await update.message.reply_text("Search for a game first with /add")
        return
    try:
        choice = int(update.message.text) - 1
        selected = results[choice]
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid choice.")
        return
    watchlist = load_watchlist()
    watchlist.append({"title": selected["title"], "nsuid": selected["nsuid"]})
    with open(WATCH_FILE, "w") as f:
        json.dump(watchlist, f, indent=2)
    await update.message.reply_text(f"Added {selected['title']} to watchlist!")

async def list_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    watchlist = load_watchlist()
    if not watchlist:
        await update.message.reply_text("Your watchlist is empty.")
        return
    response = "Your watchlist:\n"
    for i, game in enumerate(watchlist):
        response += f"{i+1}. {game['title']}\n"
    await update.message.reply_text(response)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /remove <number>")
        return
    watchlist = load_watchlist()
    try:
        index = int(context.args[0]) - 1
        removed = watchlist.pop(index)
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid number.")
        return
    with open(WATCH_FILE, "w") as f:
        json.dump(watchlist, f, indent=2)
    await update.message.reply_text(f"Removed {removed['title']} from watchlist.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_games))
app.add_handler(CommandHandler("remove", remove))

from telegram.ext import MessageHandler, filters
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pick))

if __name__ == "__main__":
    print("Bot running...")
    app.run_polling()