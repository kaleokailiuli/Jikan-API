import requests as re
import json
import os
from pathlib import Path


# API configuration
BASE_URL = "https://api.jikan.moe/v4"
ANIME_ENDPOINT = "/anime"
DATA_FOLDER = Path(__file__).parent.parent.parent / "data"

# Create data folder if it dont exist
DATA_FOLDER.mkdir(exist_ok=True)

class AnimeController:
    def __init__(self):
        self.favorites_file = DATA_FOLDER / "favorites.json"
        self.cache_file = DATA_FOLDER / "search_cache.json"
        self.settings_file = DATA_FOLDER / "settings.json"
    
    def fetch_anime_from_api(self, search_query):
        # Get anime from API
        try:
            url = f"{BASE_URL}{ANIME_ENDPOINT}?q={search_query}&limit=10"
            response = re.get(url, timeout=5, verify=False)
            response.raise_for_status()
            data = response.json()
            
            if data.get("data"):
                return data.get("data")
            else:
                return None
                
        except re.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def parse_anime_data(self, raw_api_data):
        parsed_results = []
        
        for anime in raw_api_data:
            anime_item = {
                "id": anime.get("mal_id"),
                "title": anime.get("title"),
                "episodes": anime.get("episodes"),
                "overview": anime.get("synopsis"),
                "rating": anime.get("score"),
                "image_url": anime.get("images", {}).get("jpg", {}).get("image_url")
            }
            parsed_results.append(anime_item)
        
        return parsed_results
    
    def save_to_file(self, data, filename):
        # Save data as JSON
        try:
            filepath = DATA_FOLDER / filename
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def load_from_file(self, filename):
        # Load data from JSON file
        try:
            filepath = DATA_FOLDER / filename
            if filepath.exists():
                with open(filepath, "r") as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading file: {e}")
            return []
    
    def get_favorites(self):
        # Load favorites list
        return self.load_from_file("favorites.json")
    
    def add_to_favorites(self, anime):
        # Add anime to favorites if not duplicate
        favorites = self.get_favorites()
        
        for fav in favorites:
            if fav.get("id") == anime.get("id"):
                return False
        
        favorites.append(anime)
        self.save_to_file(favorites, "favorites.json")
        return True
    
    def remove_from_favorites(self, anime_id):
        # Remove anime from favorites
        favorites = self.get_favorites()
        favorites = [fav for fav in favorites if fav.get("id") != anime_id]
        self.save_to_file(favorites, "favorites.json")
    
    def search_anime(self, search_query):
        # Check cache first, then try API
        cache = self.load_from_file("search_cache.json")
        
        for cached_search in cache:
            if cached_search.get("query") == search_query:
                print("Using cached results")
                return cached_search.get("results")
        
        api_data = self.fetch_anime_from_api(search_query)
        
        if api_data:
            parsed = self.parse_anime_data(api_data)
            
            cache.append({
                "query": search_query,
                "results": parsed
            })
            self.save_to_file(cache, "search_cache.json")
            
            return parsed
        else:
            print("API failed, no cached results")
            return None


# Test both functions
if __name__ == '__main__':
    controller = AnimeController()
    
    # Test API call
    print("Testing API call...")
    api_results = controller.fetch_anime_from_api("Attack on Titan")
    
    if api_results:
        print(f"API call successful! Found {len(api_results)} results")
        
        # Test parse and store
        print("Parsing and storing data...")
        parsed_data = controller.parse_anime_data(api_results)
        controller.save_to_file(parsed_data, "test_results.json")
        
        print("Test complete!")
    else:
        print("API call failed")
