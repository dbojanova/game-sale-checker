import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from nintendo_search import search_nintendo_id
from add_games import load_watchlist, WATCH_FILE
from notifier import TOKEN

#make sure that these commands are onlt used in the group chat, not in DMs with the bot
def is_group(update: Update) -> bool:
    return str(update.effective_chat.id) == os.getenv("TELEGRAM_CHAT_EDITS")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /add <game name>")
        return
    query = " ".join(context.args)
    results = search_nintendo_id(query)
    if not results:
        await update.message.reply_text("No results found - check spelling.")
        return
    response = "Pick a game (or multiple, e.g. 1,3 — or 0 to cancel):\n"
    for i, game in enumerate(results):
        response += f"{i+1}. {game['title']} (nsuid: {game['nsuid']})\n"
    context.user_data["results"] = results
    await update.message.reply_text(response)

async def pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        return
    results = context.user_data.get("results")
    if not results:
        await update.message.reply_text("Search for a game first with /add")
        return
    text = update.message.text.strip()
    if text == "0":
        context.user_data["results"] = None
        await update.message.reply_text("Cancelled.")
        return
    try:
        watchlist = load_watchlist()
        added = []
        for choice in text.split(","):
            index = int(choice.strip()) - 1
            selected = results[index]
            watchlist.append({"title": selected["title"], "nsuid": selected["nsuid"]})
            added.append(selected["title"])
        with open(WATCH_FILE, "w") as f:
            json.dump(watchlist, f, indent=2)
        context.user_data["results"] = None
        await update.message.reply_text("Added:\n" + "\n".join(added))
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid choice — send numbers like 1 or 1,3")

async def list_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        return
    watchlist = load_watchlist()
    if not watchlist:
        await update.message.reply_text("Your watchlist is empty.")
        return
    response = "Your watchlist:\n"
    for i, game in enumerate(watchlist):
        response += f"{i+1}. {game['title']}\n"
    await update.message.reply_text(response)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /remove <game title>")
        return
    query = " ".join(context.args).lower()
    watchlist = load_watchlist()
    match = next((g for g in watchlist if g["title"].lower() == query), None)
    if not match:
        await update.message.reply_text(f"No game found matching '{query}'.")
        return
    watchlist.remove(match)
    with open(WATCH_FILE, "w") as f:
        json.dump(watchlist, f, indent=2)
    await update.message.reply_text(f"Removed {match['title']} from watchlist.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_games))
app.add_handler(CommandHandler("remove", remove))

from telegram.ext import MessageHandler, filters
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pick))

if __name__ == "__main__":
    print("Bot running...")
    app.run_polling(timeout=30)
