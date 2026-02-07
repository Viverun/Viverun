import re
import json
import csv
import io
import random
import requests

# Keywords to strictly filter for space-themed quotes
KEYWORDS = [
    "cosmos", "universe", "astronomy", "planet", "galaxy", 
    "telescope", "physics", "nebula", "black hole", "gravity",
    "orbit", "celestial", "constellation", "eclipse", "moon", "sun",
    "mars", "jupiter", "saturn", "venus", "mercury", "pluto", "neptune",
    "uranus", "comet", "asteroid", "meteor", "extraterrestrial",
    "astronaut", "nasa", "spacex", "interstellar", "light year", "quasar",
    "supernova", "big bang", "dark matter", "solar system", "milky way", "andromeda",
    "hubble", "voyager", "apollo", "sputnik", "curiosity", "perseverance",
    "science", "relativity", "quantum", "multiverse", "wormhole", 
    "event horizon", "singularity", "pulsar", "neutron star", "white dwarf", 
    "red giant", "supergiant", "exoplanet", "astrophysics", "cosmology"
]

# Keywords to EXCLUDE (to avoid metaphorical usage like "love the moon")
NEGATIVE_KEYWORDS = [
    "love", "romance", "marriage", "baby", "business", "money", "politics", 
    "success", "dream", "god", "heaven", "hell", "angel", "soul", "spirit",
    "leadership", "management", "investing", "finance", "dating", "relationship",
    "sex", "kiss", "heart", "emotion", "feeling", "football", "soccer", "sport",
    "game", "play", "win", "lose", "rich", "poor", "economy", "market",
    "actor", "actress", "movie", "film", "music", "song", "dance", "party",
    "fashion", "style", "beauty", "makeup", "hair", "dress", "clothes",
    "food", "drink", "eat", "cook", "chef", "kitchen", "recipe", "diet",
    "code", "programming", "software", "developer", "bug", "computer" 
]

# Sources
JSON_SOURCES = [
    "https://raw.githubusercontent.com/JamesFT/Database-Quotes-JSON/master/quotes.json",
    "https://raw.githubusercontent.com/shpeley/quotes/master/quotes.json",
    "https://raw.githubusercontent.com/dwyl/quotes/main/quotes.json"
]

CSV_SOURCES = [
    "https://gist.githubusercontent.com/JakubPetriska/060958fd744ca34f099e947cd080b540/raw/quotes.csv",
    "https://raw.githubusercontent.com/jcalazan/random-quotes/master/db/randomquotes.csv",
    "https://raw.githubusercontent.com/akhiltak/inspirational-quotes/master/Quotes.csv"
]

TXT_SOURCES = [
    "https://raw.githubusercontent.com/alvations/Quotables/master/author-quote.txt"
]

def is_space_themed(text):
    if not text:
        return False
    text = text.lower()
    
    # 1. Regex check for Negative Keywords (strict word boundary)
    for neg in NEGATIVE_KEYWORDS:
        if re.search(r'\b' + re.escape(neg) + r'\b', text):
            return False
            
    # 2. Regex check for Positive Keywords
    match_found = False
    for keyword in KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            match_found = True
            break
    
    if not match_found:
        return False
        
    return True

def harvest_quotes():
    all_quotes = []
    seen_quotes = set()
    MAX_TOTAL_QUOTES = 800 # Keep file size manageable for API
    
    # Priority Hardcoded Quotes
    hardcoded = [
        {"quote": "We are a way for the cosmos to know itself.", "author": "Carl Sagan"},
        {"quote": "The universe is under no obligation to make sense to you.", "author": "Neil deGrasse Tyson"},
        {"quote": "Look up at the stars and not down at your feet.", "author": "Stephen Hawking"},
        {"quote": "Somewhere, something incredible is waiting to be known.", "author": "Carl Sagan"},
        {"quote": "Space is big. You just won't believe how vastly, hugely, mind-bogglingly big it is.", "author": "Douglas Adams"},
        {"quote": "The history of astronomy is a history of receding horizons.", "author": "Edwin Hubble"},
        {"quote": "Equipped with his five senses, man explores the universe around him and calls the adventure Science.", "author": "Edwin Hubble"},
        {"quote": "The Nitrogen in our DNA, the Calcium in our teeth, the Iron in our blood, the Carbon in our apple pies were made in the interiors of collapsing stars. We are made of starstuff.", "author": "Carl Sagan"}
    ]
    
    for item in hardcoded:
        all_quotes.append(item)
        seen_quotes.add(item['quote'])

    # Helper function to add valid quotes
    def add_if_valid(quote, author):
        if not quote: return
        # Clean up
        q_clean = quote.strip()
        a_clean = author.strip() if author else "Unknown"
        
        # Validation checks
        if len(q_clean) > 250: return # Too long for a card
        if len(q_clean) < 10: return  # Too short
        if q_clean in seen_quotes: return
        if not is_space_themed(q_clean): return
        
        all_quotes.append({"quote": q_clean, "author": a_clean})
        seen_quotes.add(q_clean)

    # 1. Fetch JSON datasets
    for url in JSON_SOURCES:
        try:
            print(f"Fetching {url}...")
            response = requests.get(url, timeout=30)
            if response.status_code != 200: continue
            
            data = response.json()
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                if "quotes" in data and isinstance(data["quotes"], list):
                    items = data["quotes"]
                else:
                    items = [data]
            
            for item in items:
                q = item.get('quoteText') or item.get('quote') or item.get('text') or item.get('body')
                a = item.get('quoteAuthor') or item.get('author')
                add_if_valid(q, a)
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # 2. Fetch CSV datasets
    for url in CSV_SOURCES:
        try:
            print(f"Fetching {url}...")
            response = requests.get(url, timeout=30)
            if response.status_code != 200: continue
            
            csv_content = response.content.decode('utf-8', errors='ignore')
            delimiter = ';' if ';' in csv_content[:100] and csv_content[:100].count(';') > csv_content[:100].count(',') else ','
            csv_reader = csv.reader(io.StringIO(csv_content), delimiter=delimiter)
            
            for row in csv_reader:
                if len(row) >= 2:
                    add_if_valid(row[0], row[1])
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    # 3. Fetch TXT datasets
    for url in TXT_SOURCES:
        try:
            print(f"Fetching {url}...")
            response = requests.get(url, timeout=30)
            if response.status_code != 200: continue
            content = response.text
            
            for line in content.splitlines():
                if '-' in line:
                    parts = line.split('-', 1)
                    if len(parts) == 2:
                        add_if_valid(parts[1], parts[0])
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    # Shuffle and trim
    # Prioritise keeping the hardcoded ones at the start? No, shuffle is better for randomness
    # But let's guarantee hardcoded ones are in the final set if we trim.
    
    final_set = all_quotes[:MAX_TOTAL_QUOTES]
    random.shuffle(final_set)
    
    print(f"Harvested {len(all_quotes)} total candidates.")
    print(f"Saving {len(final_set)} unique space-themed quotes.")
    
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(final_set, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    harvest_quotes()
