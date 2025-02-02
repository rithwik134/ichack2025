import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup

PRIMARY = ' Profile Sections Local tv Featured More From NBC Follow NBC News news Alerts There are no new alerts at this time After shares of Tesla dipped by more than 10% on Tuesday deepening a year-long selloff, CEO Elon Musk told employees not to be “too bothered by stock market craziness.” Musk circulated the comments on Wednesday in a companywide email, which CNBC obtained. He told staffers that Tesla needs to “demonstrate continued excellent performance,” and that “long-term, I believe very much that Tesla will be the most valuable company on Earth!” Electric vehicle blog Electrek reported earlier on the email. Tesla shares have declined about 68% for the year, though they rose 3.3% on Wednesday to $112.71. The stock is down 42% in December, and is poised to close out its worst month, quarter and year on record . Musk has blamed Tesla’s declining share price in part on rising interest rates. But critics point to his Twitter takeover as a bigger culprit for the slide, which has wiped out about $675 billion in market cap this year as of Wednesday’s close. In the email, Musk thanked Tesla employees for their work in 2022, encouraged them to push hard for a strong fourth-quarter finish, and asked them to “volunteer to help deliver” cars to customers before midnight on Dec. 31, if at all possible. During the last days of most quarters, Tesla enlists employees from all over the company to bring new cars to customers in order to hit or exceed stated delivery goals, work that in normal times is limited to people on the sales and delivery teams. The company has been aiming for 50% year-over-year growth in vehicle deliveries but has cautioned investors it may not meet that target every year. Musk’s attention has been focused on Twitter of late. The Tesla and SpaceX CEO sold tens of billions of dollars worth of shares in his electric vehicle company in 2022 to finance the $44 billion buyout of the social media company. ©\xa02025 NBCUniversal Media, LLC'
url = "https://i.imgur.com/5bGzZi7.jpg"
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
            f"You need to compare the content of two articles. One will be the <PRIMARY> article, and the other the <COMPARISON> article.\n\nThe articles will be pasted below as text dumps, scraped from the webpages’ HTML. Consider contextually the **relevant** information from each page, discarding useless info such as headers, text which appears to have been scraped from sidebars, etc.\n\nYour objective is is to compare the relevancy of the two articles. Produce a short summary of no more than 100 words, explaining the topic and content of the <COMPARISON> article. Describe in this whether or not it is directly relevant to the topic of the <PRIMARY> content. For example, if the <PRIMARY> content relates to a forest fire in 2024, but the <COMPARISON> content is about a forest fire in 2021, then explain how the <COMPARISON> content is about a wholly different event and therefore is not relevant. We are doing this to combat the spread of misinformation, which you should consider.\nRespond using pure JSON, with a single field called Summary, into which the summary will be output.\n---n<PRIMARY>\n{PRIMARY}\n<\\PRIMARY>\n\n<COMPARISON>\n{COMPARISON}\n<\\COMPARISON>",
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

breakpoint()

app = Flask(__name__)

@app.route('/')
def status():
    return jsonify({"status": "ok"})

@app.route('/process', methods=['GET'])
def process():
    url = request.json['image_url']
    url = scrape_text(request.json['url'])
    return summing(rev(url))


if __name__ == '__main__':
    app.run(debug=True)