from web3 import Web3, HTTPProvider
from etherscan.accounts import Account
from etherscan.contracts import Contract
import json
import pandas as pd
import provider
import requests
from bs4 import BeautifulSoup


def get_web3_provider():
    web3_provider = 'https://mainnet.infura.io/H10eLeRZQOrGY8600d1Y'
    web3 = Web3(HTTPProvider(web3_provider))
    return web3

def ico_chart_data(token_name):
    key = 'F3C5GJBZ611TXR77PFERXB56R5VD1P9YUD'
    try:
        address = provider.search(token_name)['ico']
        web3 = get_web3_provider()
        account = Account(address=address, api_key=key)
        transactions = account.get_all_transactions(offset=10000, sort='asc', internal=True)

        data_frame = pd.DataFrame(transactions)
        data_frame = data_frame[(data_frame['isError'] != '1')]
        data_frame['datetime'] = pd.to_datetime(data_frame['timeStamp'], unit='s')
        data_frame['value'] = data_frame['value'].apply(lambda x: web3.fromWei(int(x), 'ether'))
        data_frame = data_frame[data_frame['value'] > 0]
        data_frame['date'] = data_frame['datetime'].dt.date
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
        return labels, cumulative_values
    except:
        return None


def holders_chart_data(token_name, count):
    etherscan_link = 'https://etherscan.io/token/tokenholderchart/{}?range={}'
    try:
        address = provider.search(token_name)['token']
        response = requests.get(etherscan_link.format(address, count)).content.decode('utf-8')
        soup = BeautifulSoup(response, 'html.parser')
        tds = soup.find(id='ContentPlaceHolder1_resultrows').find('tbody').find_all('td')
        labels = []
        values = []
        top_percentage = 0
        for i in range(count):
            address = tds[i*4+1].find('a').text
            percentage = tds[i*4+3].text[:-1]
            percentage = float(percentage[:percentage.find('.') + 3])
            labels.append(address)
            values.append(percentage)
            top_percentage += percentage
        labels.append('others')
        values.append(100 - top_percentage)
        return labels, values
    except:
        return None


def token_summary_data(token_name):
    link = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD,BTC'
    try:
        symbol = provider.symbol(token_name)
        response = requests.get(link.format(symbol)).content.decode('utf-8')
        response = json.loads(response)
        response = response['RAW'][symbol]
        price_usd = response['USD']['PRICE']
        price_btc = response['BTC']['PRICE']
        total_volume = response['USD']['TOTALVOLUME24H']
        change_percent = response['USD']['CHANGEPCT24HOUR']
        market_cap = response['USD']['MKTCAP']
        return price_usd, price_btc, total_volume, market_cap, change_percent
    except:
        return None

def project_links(token_name):
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

# usage:
# ico_chart_data('aragon')
# holders_chart_data('aragon', 5)
# token_summary_data('aragon')
# project_links('aragon')
# reputation('aragon')