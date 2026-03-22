import html
import json
import random
import re

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

        quote = html.escape(str(quote_data["quote"]).strip())
        author_value = quote_data.get("author") or "Unknown"
        author = html.escape(str(author_value).strip() or "Unknown")
        print(f"Selecting quote: {quote_data['quote']}")

        new_block = (
            "<!-- START_QUOTE -->\n"
            f"<p><em>{quote}</em><br/><sub>{author}</sub></p>\n"
            "<!-- END_QUOTE -->"
        )
        
        # Read file
        with open(self.readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex replacement between markers
        pattern = r'<!-- START_QUOTE -->.*?<!-- END_QUOTE -->'
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
