from provider import TokenInfoProvider

token_name = 'aragon'
token = TokenInfoProvider(token_name)
print(token.info)
print(token.links)