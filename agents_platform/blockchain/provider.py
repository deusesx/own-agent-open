import json
import requests
from bs4 import BeautifulSoup


# get trader info from coinmarketcap
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

# get ofiicial links from etherscan

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


def links(token_name):
    etherscan_link = 'https://etherscan.io/token/'
    try:
        response = requests.get(etherscan_link + token_name).content.decode('utf-8')
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.find(id='ContentPlaceHolder1_tr_officialsite_2').find_all('a')
        items = {}
        for link in links:
            title = link.get('data-original-title')
            name = title[:title.find(':')].lower()
            if name == 'coinmarketcap':
                url = link.get('href')
            else:
                url = title[title.find(':') + 2:]
            items.update({name: url})
        return items
    except:
        return None

# returns a reputation of token from etherscan
def reputation(token_name):
    etherscan_link = 'https://etherscan.io/token/'
    try:
        response = requests.get(etherscan_link + token_name).content.decode('utf-8')
        soup = BeautifulSoup(response, 'html.parser')
        reputation = soup.find('a', attrs={
            'href':'https://etherscancom.freshdesk.com/support/solutions/articles/35000022146-etherscan-token-reputation-system'
            }).text
        return reputation
    except:
        return None


# makes an ethereum address from token name
def address(token_name):
    etherscan_link = 'https://etherscan.io/token/'
    try:
        response = requests.get(etherscan_link + token_name).content.decode('utf-8')
        soup = BeautifulSoup(response, 'html.parser')
        address = soup.find(id='ContentPlaceHolder1_trContract').find('a').text
        return address
    except:
        return None