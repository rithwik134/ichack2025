
import requests
from bs4 import BeautifulSoup

def scrape_text(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for bad status codes
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all <p> tags
        p_tags = soup.find_all("p")
        
        # Extract text from each <p> tag and join with space
        text_list = [p.get_text(separator=' ', strip=True) for p in p_tags]
        text = " ".join(text_list)

        return text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"



from serpapi import GoogleSearch

# Set up the SerpApi client with the proper parameters
params = {
    "api_key": "6c9774f99efed2498c69fd9b4a685c5180ec837182aa637aa9d64472d9150d68",
    "engine": "yandex_images",
    "url": "https://i.imgur.com/5bGzZi7.jpg"
}

# Make the API request
search = GoogleSearch(params)
results = search.get_dict()
things = []
# Iterate over image results and print each original image link
if 'image_results' in results:
    for image in results['image_results'][:3]:
        link = image.get('link')
        things.append((link, scrape_text(link)))
else:
    print("No image results found.")

print(things)