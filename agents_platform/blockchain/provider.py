import json
import requests
from bs4 import BeautifulSoup
from web3 import Web3, HTTPProvider
from etherscan.accounts import Account
from etherscan.contracts import Contract
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

# creates a picture with ico plot in it
def plot_ico_cummulative(address):
    try:
        web3_provider = 'https://mainnet.infura.io/H10eLeRZQOrGY8600d1Y'
        key = 'F3C5GJBZ611TXR77PFERXB56R5VD1P9YUD'

        web3 = Web3(HTTPProvider(web3_provider))

        abi = json.loads(Contract(address=address, api_key=key).get_abi())

        account = Account(address=address, api_key=key)
        transactions = account.get_all_transactions(offset=10000, sort='asc', internal=True)

        data_frame = pd.DataFrame(transactions)
        data_frame = data_frame[(data_frame['isError'] != '1')]
        data_frame['datetime'] = pd.to_datetime(data_frame['timeStamp'], unit='s')
        data_frame['date'] = data_frame['datetime'].dt.date
        # data_frame['value'] = pd.to_numeric(data_frame['value'], errors='coerce').astype(np.uint64)
        data_frame['value'] = data_frame['value'].apply(lambda x: web3.fromWei(int(x), 'ether'))
        data_frame = data_frame[data_frame['value'] > 0]
        data_frame['blockNumber'] = data_frame['blockNumber'].apply(lambda x: int(x))
        data_group = data_frame.groupby('blockNumber')['value', 'isError'].sum()
        data_group['index'] = data_group.index

        labels = data_group['index'].as_matrix()
        min_label = labels.min()
        max_label = labels.max()
        labels = (labels - min_label) * 100 / (max_label - min_label)
        values = data_group['value'].as_matrix()
        cumulative_values = values.cumsum()
        total = values.sum()
        cumulative_values = cumulative_values * 100 / total

        fig, ax = plt.subplots()
        high_line = [(0.8 * x + 20) for x in labels]
        low_line = [(10 / 8 * x - 25) if (10 / 8 * x - 25) > 0 else 0 for x in labels]
        top_line = [100 for x in labels]
        # Plot lines on graph
        l1, = ax.plot(labels, high_line, '#33CC14')
        l2, = ax.plot(labels, low_line, '#FFFF00')
        l3, = ax.plot(labels, cumulative_values)
        plt.fill_between(labels, top_line, high_line, alpha=.5, color='#33CC14')
        plt.fill_between(labels, high_line, low_line, alpha=.5, color='#FFFF00')
        plt.fill_between(labels, low_line, alpha=.5, color='#FF0000')

        fig.savefig("picture.png", bbox_inches='tight')
        return True
    except:
        return False

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