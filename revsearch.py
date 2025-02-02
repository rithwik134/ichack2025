import requests
from flask import Flask, jsonify, request
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

        # Find the first <img> tag
        img_tag = soup.find("img")
        
        img_url = None
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            # Handle relative URLs
            if not img_url.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                img_url = urljoin(url, img_url)

        return (text, img_url)
    except requests.exceptions.RequestException as e:
        return (f"Error: {e}", None)

from serpapi import GoogleSearch
url = input()
PRIMARY = (scrape_text(url))[0]
img = (scrape_text(url))[1]

def rev(url):
    # Set up the SerpApi client with the proper parameters
    params = {
        "api_key": "6c9774f99efed2498c69fd9b4a685c5180ec837182aa637aa9d64472d9150d68",
        "engine": "yandex_images",
        "url": url
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

    return things

import google.generativeai as genai
import typing_extensions as typing


import json
class Summary(typing.TypedDict):
    summary: str

def summing(array):
    summs = []
    for i in array:
        COMPARISON = i[1]
        genai.configure(api_key="AIzaSyAvE_BFltsv9TFA91ZbFJBUJmtKlj9Gu0Q")
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content(
            f"You need to compare the content of two articles. One will be the <PRIMARY> article, and the other the <COMPARISON> article.\n\nThe articles will be pasted below as text dumps, scraped from the webpages’ HTML. Consider contextually the **relevant** information from each page, discarding useless info such as headers, text which appears to have been scraped from sidebars, etc.\n\nYour objective is is to compare the relevancy of the two articles. Produce a short summary of no more than 100 words, explaining the topic and content of the <COMPARISON> article. Describe in this whether or not it is directly relevant to the topic of the <PRIMARY> content. For example, if the <PRIMARY> content relates to a forest fire in 2024, but the <COMPARISON> content is about a forest fire in 2021, then explain how the <COMPARISON> content is about a wholly different event and therefore is not relevant. We are doing this to combat the spread of misinformation, which you should consider. Consider, for example, whether attributes like locations match between sources; if they don't, it implies a lack of credubility.\nRespond using pure JSON, with a single field called Summary, into which the summary will be output.\n---n<PRIMARY>\n{PRIMARY}\n<\\PRIMARY>\n\n<COMPARISON>\n{COMPARISON}\n<\\COMPARISON>",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=Summary
            ),
        )
        # Extract summary from JSON response
        summary_string = result.candidates[0].content.parts[0].text
        summary_dict = json.loads(summary_string)
        summs.append(summary_dict['summary'])

    genai.configure(api_key="AIzaSyDyMut8EfJll8fx4s4o1r6-EsVM1br7Gpc")
        # For the second Gemini call, just get the text directly
    newsumm = model.generate_content(f"We have been given an image. We found three other articles which include the image. I will include summaries of those articles which explain how relevant they are to the current article, from which we took the image. **IN NO MORE THAN 100 WORDS**, with no fluff or introduction, compile the three. For example, start by saying how we found this image in 3 other locations, and then condense the summary of each relevant location, saying whether or not the articles were relevant or not. Provide an overall judgement within the 100 words of whether our image seems to be used in relevant, credible contexts or not.\n\n---\n<ARTICLE1>\n{summs[0]}\n<\\ARTICLE1>\n\n<ARTICLE2>\n{summs[1]}\n<\\ARTICLE2>\n\n<ARTICLE3>\n{summs[2]}\n<\\ARTICLE3>\n<CURRENT>\n{PRIMARY}\n<\\CURRENT>",
    generation_config=genai.GenerationConfig())
    final_summary = newsumm.candidates[0].content.parts[0].text
    return final_summary

def main():
    print(summing(rev((scrape_text(url))[1])))

main()
