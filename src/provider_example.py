from provider import TokenInfoProvider

# good for parsing: aragon, golem, civic, qtum, eos, storj
token_name = 'golem'

# some tokens don't have a shortcut name at etherscan
# in this cases it's better to specify its address manually and pass it to constructor
# token_addr = '0xd697A61D5FB4e076125e0bE647f902b02bb3A0F1'

token = TokenInfoProvider(token_name)
print(token.info)
print(token.links)
print(token.reputation)