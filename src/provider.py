import json
import requests
from bs4 import BeautifulSoup

class TokenInfoProvider:
	cmc_link = 'https://api.coinmarketcap.com/v1/ticker/'
	etherscan_link = 'https://etherscan.io/token/'

	def __init__(self, token_name, token_address=''):
		self.token_name = token_name
		self.token_address = token_address

	@property
	# get trader info from coinmarketcap
	def info(self):
		try:
			response = json.loads(requests.get(self.cmc_link + self.token_name).content.decode('utf-8'))
			return response[0]
		except:
			return None

	@property
	# get ofiicial links from etherscan
	def links(self):
		token_url = self.etherscan_link
		if self.token_address:
			token_url += self.token_address
		else:
			token_url += self.token_name
		try:
			response = requests.get(token_url).content.decode('utf-8')
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

	@property
	def reputation(self):
		token_url = self.etherscan_link
		if self.token_address:
			token_url += self.token_address
		else:
			token_url += self.token_name
		try:
			response = requests.get(token_url).content.decode('utf-8')
			soup = BeautifulSoup(response, 'html.parser')
			reputation = soup.find('a', attrs={
				'href':'https://etherscancom.freshdesk.com/support/solutions/articles/35000022146-etherscan-token-reputation-system',
				'title':'Click for more info'}).text
			return reputation
		except:
			return None