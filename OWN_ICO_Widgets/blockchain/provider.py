import json
import requests
from bs4 import BeautifulSoup


def symbol(token_name):
    cryptocompare_link = 'https://www.cryptocompare.com/api/autosuggest/all/?maxRows=1&q='
    try:
        response = json.loads(requests.get(cryptocompare_link + token_name).content.decode('utf-8'))
        symbol = response['Results'][0]['nodeName']
        symbol = symbol[symbol.find('('):].replace('(', '').replace(')', '')
        if len(symbol) < 3:
            return None
        return symbol
    except:
        return None

def search(query):
    search_link = 'https://etherscan.io/searchHandler?term='
    response = requests.get(search_link + query).content.decode('utf-8').replace('"', '').replace('[', '')
    results = {}
    for item in response.split(','):
        name = item[:item.find('\\t')]
        item = item[item.find('\\t')+2:]
        address = item[:item.find('\\t')]
        results.update({name: address})
    
    addresses = {}
    found_best = False
    for key in results:
        if 'sale' in key.lower() or 'ico' in key.lower() or 'auction' in key.lower():
            addresses.update({'ico': results[key]})
        elif (query + ' (' in key.lower() or 'token' in key.lower()) and not found_best:
            if query + ' (' in key.lower():
                found_best = True
            addresses.update({'token': results[key]})
    return addresses