import requests
from add_games import load_watchlist
from notifier import send_notification

WATCH_FILE = "watchlist.json"

def check_nintendo_price(game_name, id):
	url=f"https://api.ec.nintendo.com/v1/price?country=US&lang=en&ids={id}"
	response=requests.get(url)
	result=response.json()

	price = result["prices"][0]

	if price["sales_status"]!="onsale":
		print(f"{game_name} not available for Switch.")
		return
	
	if "discount_price" in price:
		normal=price["regular_price"]["amount"]
		sale=price["discount_price"]["amount"]
		send_notification(f"{game_name} is on sale for Switch: {sale} rather than  {normal}")
		print(f"{game_name} is on sale for Switch!")
	else:
		print(f"Nothing on sale at the moment.")

if __name__=="__main__":
	watchlist = load_watchlist()
	if not watchlist:
		print("No watchlist set at the moment.")
	else:
		for game in watchlist:
			check_nintendo_price(game['title'],game['nsuid'])
