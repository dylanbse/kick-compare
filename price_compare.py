from bs4 import BeautifulSoup
import requests


def ebay_format(link):
    ebay_request = requests.get(link)
    soup = BeautifulSoup(ebay_request.text, 'html.parser')

    span_tags = soup.find_all('span')
    for span in span_tags:
        try:
            if span['id'] == 'prcIsum':
                print(span["content"])
        except KeyError:
            continue

def fl_format(link):
    fl_request = requests.get(link)
    soup = BeautifulSoup(fl_request.text, 'html.parser')

    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        try:
            if meta['itemprop'] == 'price':
                print(meta["content"])
        except KeyError:
            continue


def kickz_format(link):
    user_agent = 'Mozilla/5.0'
    headers = {'user-agent': user_agent}
    kickz_request = requests.get(link, headers=headers)
    soup = BeautifulSoup(kickz_request.text, 'html.parser')

    name = soup.find(id='prodNameId').text
    print(name)

    item_div = soup.find(id='normalPriceId')
    span = item_div.find(itemprop='price')
    print(span.text)


kickz_format('https://www.kickz.com/uk/jordan-sandals-and-flip-flops-jordan-crater-slide-black_university_red_green_spark_white-168795001')