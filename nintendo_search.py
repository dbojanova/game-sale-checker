import requests
import json
import os
import time

NSUID_FILE = "titledb_cache.json"
TITLEDB_URL = "https://raw.githubusercontent.com/blawar/titledb/master/US.en.json"
IGNORE_WORDS = {"of","the","a","an","and","in","to","for"}

def pull_titledb():

    #update database every week
    if os.path.exists(NSUID_FILE):
        time_elapsed = time.time() - os.path.getmtime(NSUID_FILE)
        if time_elapsed > 7 * 24 * 60 * 60:
            print("Updating database!")
            os.remove(NSUID_FILE)

    if not os.path.exists(NSUID_FILE):
        response = requests.get(TITLEDB_URL)
        with open(NSUID_FILE, "w") as f:
            json.dump(response.json(), f)
    with open(NSUID_FILE, "r") as f:
        return json.load(f)

def search_nintendo_id(query):
    db = pull_titledb()
    query_words = query.lower().split()
    search_words = [w for w in query_words if w not in IGNORE_WORDS]
    
    hits = []

    for nsuid, game in db.items():
        name = game.get("name", "")
        if not name:
            continue
        lower_name = name.lower()
        if all(word in lower_name for word in search_words):
            hits.append({"title": name, "nsuid": nsuid})
    
    # some games aren't in the API - allow manual entry
    if not hits:
        if __name__ == "__main__":
            print("Game not found.")
            choice = input("Add it manually? 1. Yes 2. No\n>")
            if choice == "1":
                title = input("Game Title (full):")
                nsuid = input("NSUID (14 digits):")
                hits = [{"title": title, "nsuid": nsuid}]
            else:
                return []
        else:
            return []

    return hits
