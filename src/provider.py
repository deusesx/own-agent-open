import json
import requests
from bs4 import BeautifulSoup

class TokenInfoProvider:
	cmc_link = 'https://api.coinmarketcap.com/v1/ticker/'
	etherscan_link = 'https://etherscan.io/token/'

	def __init__(self, token_name):
		self.token_name = token_name

	@property
	# get trader info from coinmarketcap
	def info(self):
		response = json.loads(requests.get(self.cmc_link + self.token_name).content.decode('utf-8'))
		return response[0]

	@property
	# get ofiicial links from etherscan
	def links(self):
		response = requests.get(self.etherscan_link + self.token_name).content.decode('utf-8')
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