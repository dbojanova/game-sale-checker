import requests
import json

ALGOLIA_URL="https://u3b6gr4ua3-dsn.algolia.net/1/indexes/ncom_game_en_us"
ALGOLIA_APP_ID="U3B6GR4UA3"
ALGOLIA_API_KEY="c4da8be7fd29f0f5bfa42920b0a99dc7"
IGNORE_WORDS = {"of","the","a","an","and","in","to","for"}

def search_nintendo_id(query):
    query_words = query.lower().split()
    search_words = [w for w in query_words if w not in IGNORE_WORDS]

    params = {
        "query": query,
        "hitsPerPage": 100,
        "x-algolia-application-id": ALGOLIA_APP_ID,
        "x-algolia-api-key": ALGOLIA_API_KEY,
    }

    response = requests.get(ALGOLIA_URL, params=params)
    result = response.json()
    
    hits = []

    for hit in result["hits"]:
        if hit["platform"] == "Nintendo Switch" and hit.get("nsuid"):
            lower_title = hit["title"].lower()
            if all(word in lower_title for word in search_words):
                hits.append({"title": hit["title"], "nsuid": hit["nsuid"]})
        
        if hits:
            return hits
    
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
