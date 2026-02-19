import json
import os
from nintendo_search import search_nintendo_id

WATCH_FILE="watchlist.json"

def load_watchlist():
	if not os.path.exists(WATCH_FILE):
		return []
	with open(WATCH_FILE, "r") as f:
		return json.load(f)

def add_game():
	query=input("What game do you want to track?")
	results=search_nintendo_id(query)

	if not results:
		print("No results found - check for spelling mistakes.")

	for i,game in enumerate(results):
		print(f"{i+1}.{game['title']}(nsuid:{game['nsuid']})")

	choice=int(input("Pick the correct game(s):"))-1
	selected=results[choice]

	watchlist=load_watchlist()
	watchlist.append({
		"title":selected["title"],
		"nsuid":selected["nsuid"]
	})

	with open(WATCH_FILE, "w") as f:
		json.dump(watchlist,f,indent=2)

	print(f"Added {selected['title']} to watchlist!")

if __name__=="__main__":
	add_game()