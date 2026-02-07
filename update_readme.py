import json
import random
import re
import os
import urllib.parse
from datetime import datetime

class QuoteUpdateService:
    def __init__(self, quotes_file='quotes.json', readme_file='README.md'):
        self.quotes_file = quotes_file
        self.readme_file = readme_file

    def get_random_quote(self):
        with open(self.quotes_file, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        return random.choice(quotes) if quotes else None

    def update_readme(self):
        quote_data = self.get_random_quote()
        if not quote_data:
            print("No quotes available.")
            return

        print(f"Selecting quote: {quote_data['quote']}")
        
        # URL encode params
        quote_encoded = urllib.parse.quote(quote_data['quote'])
        author_encoded = urllib.parse.quote(quote_data['author'])
        
        # Add random seed to bust cache
        seed = int(datetime.now().timestamp())
        
        new_url = f"https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark&quote={quote_encoded}&author={author_encoded}&v={seed}"
        
        # New content block
        new_block = f'<!-- START_QUOTE -->\n<img src="{new_url}" alt="Quote"/>\n<!-- END_QUOTE -->'
        
        # Read file
        with open(self.readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex replacement between markers
        pattern = r'(<!-- START_QUOTE -->)(.*?)(<!-- END_QUOTE -->)'
        if re.search(pattern, content, flags=re.DOTALL):
            new_content = re.sub(pattern, new_block, content, flags=re.DOTALL)
            with open(self.readme_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("README updated successfully.")
        else:
            print("Markers not found in README.md")

if __name__ == "__main__":
    service = QuoteUpdateService()
    service.update_readme()
