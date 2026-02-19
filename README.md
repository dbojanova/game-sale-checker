# Is this game on sale?

Have you ever wanted a game on your Switch ... but didn't want to pay full price? Add it to a watchlist and be notified when this happens on your phone via a Telegram bot!

## Usage

**REQUIREMENTS**:
This was setup for my personal Telegram bot. If you'd like to use this repo, you must create a Telegram bot and obtain a token and chat ID(s). The scripts assume a group chat for notifications and DM with the bot for watchlist edits. Store keys in a `.env` file as such:

```.env
TELEGRAM_TOKEN="TOKEN_NUMBER" 
TELEGRAM_CHAT_EDITS="DM_CHAT_NUMBER"
TELEGRAM_CHAT_ANNOUNCEMENTS="GROUP_CHAT_NUMBER"
```

### Add/remove games to watchlist

Your watchlist will contain all the games you are interested in. This list can be edited in two ways:

(1) **TERMINAL**

To add games, run `python add_games.py` and enter the name of your game. All hits will show up, choose which to add. 

Prices are checked using game IDs, which are identified via the Algolia API. Unfortunately, some games won't have NSUID stored in Algolia. If no game hit is found, you will be prompted to manually enter the game name and NSUID. NSUID can be found on the [Nintendo EShop](https://www.nintendo.com/us/store/?srsltid=AfmBOoqZuz5ch9lGGq0usvoKDbg_tvBl3GfYK86C8Wxqks1DGaG3my3A) website.

Removal of games should be dont by manually deleting them from `watchlist.json`. Got lazy ... will add a script later for it.

(2) **PHONE** (via Telegram)

Addition, removal, and listing of games on the watchlist can be done via the Telegram bot's chat.

For this to function, `bot.py` must be actively running. To keep it running in the background, use the systemd file: `bot.service`. Make sure to change WorkingDirectory and ExecStart to your local location of the repo.

```
sudo cp bot.service /etc/systemd/system/
sudo systemctl enable bot
sudo systemctl start bot
```

Once service is running, on the Telegram chat use:

`/add` to add game
`/remove` to remove game
`/list` to see games that are tracked

## Setup regular checks

Setup a crobtab job with the included file as such (you may need to edit repo location):

`crontab regular_checks.txt`

*NOTE*: you won't be spammed with sale notifications about the same game, despite the crontab job! Games you've already been notified about will be stored in `seen.json` 