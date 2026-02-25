# Is this game on sale?

Have you ever wanted a game on your Switch ... but didn't want to pay full price? Add it to a watchlist and be notified on your phone via a Telegram bot when the game goes on sale!

NOTE: This is only for US store sales and uses the amazing database provided by [blawar](https://github.com/blawar/titledb). To change country, simply edit the `TITLEDB_URL` variable in the source code of `nintendo_checker.py` to teh appropriate country link.

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

To add games, run `python add_games.py` and enter the name of your game. All hits (name + NSUID) will show up, choose which to add. 

Game removal is done by by manually deleting them from `watchlist.json` for now. Got lazy ... will add a script later for it.

(2) **PHONE** (via Telegram)

Addition, removal, and listing of games on the watchlist can be done via the Telegram bot's chat.

To edit and see your game list in Telegram, `bot.py` must be actively running. To keep it running in the background, use the systemd file: `bot.service`. Make sure to change `WorkingDirectory` and `ExecStart` to your local repo location.

```
sudo cp bot.service /etc/systemd/system/
sudo systemctl enable bot
sudo systemctl start bot
```

Once service is running, on the Telegram chat use:

`/add` to add game
`/list` to see games that are tracked

## Setup regular checks

The `regular_checks.txt` files sets up a crontab job to check for sales every hour. If you are using a virtual python environment, please make sure to edit the location in the file (i.e. `.venv/bin/python` instead of just `python`).

Setup a crobtab job as such (you may need to edit repo location):

`crontab regular_checks.txt`

*NOTE*: you won't be spammed with sale notifications about the same game, despite the crontab job! Games you've already been notified about will be stored in `seen.json` 
