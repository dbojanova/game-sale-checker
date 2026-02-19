import requests
import json
import os
from add_games import load_watchlist
from notifier import send_notification

WATCH_FILE = "watchlist.json"
SEEN_FILE = "checked.json"

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return []
    with open(SEEN_FILE, "r") as f:
        return json.load(f)

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)

def check_nintendo_price(game_name, id):
	url=f"https://api.ec.nintendo.com/v1/price?country=US&lang=en&ids={id}"
	response=requests.get(url)
	result=response.json()

	price = result["prices"][0]
	seen = load_seen()

	if price["sales_status"]!="onsale":
		print(f"{game_name} not available for Switch.")
		if id in seen:
			seen.remove(id)
			save_seen(seen)
		return
	
	if "discount_price" in price:
		if id in seen:
			print(f"Already notified about {game_name} sale on Switch.")
			return
		normal=price["regular_price"]["amount"]
		sale=price["discount_price"]["amount"]
		send_notification(f"{game_name} is on sale for Switch: {sale} rather than  {normal}")
		print(f"{game_name} is on sale for Switch!")
		seen.append(id)
		save_seen(seen)
	else:
		print(f"Nothing on sale at the moment.")

if __name__=="__main__":
	watchlist = load_watchlist()
	if not watchlist:
		print("No watchlist set at the moment.")
	else:
		for game in watchlist:
			check_nintendo_price(game['title'],game['nsuid'])
