from bs4 import BeautifulSoup
import requests
import json


class Converter():
    def convert(link):
        store_name = get_store_name(link)
        converter = get_converter(store_name)
        product = converter(link)

        return product


def get_converter(store):
    if store == 'ebay':
        return ebay_to_json

    elif store == 'footlocker':
        return fl_to_json

    elif store == 'kickz':
        return kickz_to_json

    elif store == 'nike':
        return nike_to_json
    else:
        return 'store is invalid'


def ebay_to_json(link):
    ebay_request = requests.get(link)
    soup = BeautifulSoup(ebay_request.text, 'html.parser')

    span_tags = soup.find_all('span')
    for span in span_tags:
        try:
            if span['id'] == 'prcIsum':
                price = span["content"]
        except KeyError:
            continue
    
    h1_tag = soup.find('h1', id='itemTitle')
    h1_tag.span.extract()
    name = h1_tag.text
    return to_json(name, price)


def fl_to_json(link):
    fl_request = requests.get(link)
    soup = BeautifulSoup(fl_request.text, 'html.parser')

    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        try:
            if meta['itemprop'] == 'price':
                price = meta["content"]
        except KeyError:
            continue
    
    name = soup.find('h1', {'class': 'fl-product-details--headline'}).text
    return to_json(name, price)


def kickz_to_json(link):
    user_agent = 'Mozilla/5.0'
    headers = {'user-agent': user_agent}
    kickz_request = requests.get(link, headers=headers)
    soup = BeautifulSoup(kickz_request.text, 'html.parser')

    name = soup.find(id='prodNameId').text

    item_div = soup.find(id='normalPriceId')
    price = item_div.find(itemprop='price').text

    return to_json(name, price)


def nike_to_json(link):
    user_agent = 'Mozilla/5.0'
    headers = {'user-agent': user_agent}
    nike_request = requests.get(link, headers=headers)
    soup = BeautifulSoup(nike_request.text, 'html.parser')

    name_holder = soup.find('h1', id='pdp_product_title')
    name = name_holder.text

    price = soup.find('div', class_='product-price').text
    return to_json(name, price)


def get_store_name(link):
    name = link.split('.')
    return name[1]


def to_json(prod_name, prod_price):
    json_obj = {
        'productName': prod_name,
        'productPrice': prod_price
    }
    return json_obj


print(Converter.convert('https://www.kickz.com/uk/filling-pieces-sneakers-low-low-top-ghost-decon-brown-167332003'))
print(Converter.convert('https://www.ebay.co.uk/itm/Lacoste-Esparre-Mens-Leather-Classic-Designer-Casual-Trainers-Navy-B-Grade/293726304404?_trkparms=aid%3D1110012%26algo%3DSPLICE.SOIPOST%26ao%3D1%26asc%3D228189%26meid%3Db51750967566485793583b16d3575d2e%26pid%3D100008%26rk%3D3%26rkt%3D12%26sd%3D274422873775%26itm%3D293726304404%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DPromotedSellersOtherItemsV2%26brand%3DLacoste&_trksid=p2047675.c100008.m2219'))
print(Converter.convert('https://www.footlocker.co.uk/en/p/adidas-la-trainer-iii-s-men-shoes-92826?v=314213094304#!searchCategory=all'))
print(Converter.convert('https://www.nike.com/gb/t/air-vapormax-2020-fk-shoe-KvNhzt/CJ6741-003'))