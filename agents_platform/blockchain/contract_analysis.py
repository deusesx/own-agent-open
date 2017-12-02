from web3 import Web3, HTTPProvider
from etherscan.accounts import Account
from etherscan.contracts import Contract
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn


def get_web3_provider():
    web3_provider = 'https://mainnet.infura.io/H10eLeRZQOrGY8600d1Y'
    web3 = Web3(HTTPProvider(web3_provider))

    return web3


def get_transaction_list_of_contract(address):
    try:
        web3 = get_web3_provider()
        key = 'F3C5GJBZ611TXR77PFERXB56R5VD1P9YUD'

        abi = json.loads(Contract(address=address, api_key=key).get_abi())

        account = Account(address=address, api_key=key)
        transactions = account.get_all_transactions(offset=10000, sort='asc', internal=True)

        return transactions
    except:
        return None


def get_transaction_data_for_chart(address):
    web3 = get_web3_provider()
    transactions = get_transaction_list_of_contract(address)

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


def print_contract_history(address):
    labels, values = get_transaction_data_for_chart(address)

    fig, ax = plt.subplots()
    high_line = [(0.8 * x + 20) for x in labels]
    low_line = [(10 / 8 * x - 25) if (10 / 8 * x - 25) > 0 else 0 for x in labels]
    top_line = [100 for x in labels]
    # Plot lines on graph
    l1, = ax.plot(labels, high_line, '#33CC14')
    l2, = ax.plot(labels, low_line, '#FFFF00')
    l3, = ax.plot(labels, values)
    plt.fill_between(labels, top_line, high_line, alpha=.5, color='#33CC14')
    plt.fill_between(labels, high_line, low_line, alpha=.5, color='#FFFF00')
    plt.fill_between(labels, low_line, alpha=.5, color='#FF0000')

    fig.savefig("picture.png", bbox_inches='tight')


if __name__ == "__main__":
    print_contract_history("0x960b236A07cf122663c4303350609A66A7B288C0")
