import json

try:
    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes = json.load(f)
    print(f"Total quotes: {len(quotes)}")
    print("First 5 quotes:")
    for q in quotes[:5]:
        print(q)
    
    # Check for "love" to see if filter worked
    import re
    love_quotes = [q for q in quotes if re.search(r'\blove\b', q['quote'].lower())]
    print(f"Quotes with 'love': {len(love_quotes)}")
    if love_quotes:
        print("Example love quote:", love_quotes[0])

except Exception as e:
    print(f"Error reading quotes.json: {e}")
