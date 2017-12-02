import provider
from contract_analysis import get_contract_by_address


# good for parsing: aragon, storm, civic, eos, storj
token_name = 'leverj'

# some tokens don't have a shortcut name at etherscan
# in this cases it's better to specify its address manually

# address = provider.address(token_name)
# provider.plot_ico_cummulative('0xc88c7e1aebd89187d13bd42e1ff814d32f492bf6')

results = provider.search(token_name)
symbol = provider.symbol(token_name)
print(symbol)
if results.get('token'):
    token_address = results['token']
    links = provider.links(token_address)
    reputation = provider.reputation(token_address)
    print(links, reputation, sep='\n')
if results.get('ico'):
    plot_drawed = get_contract_by_address(results['ico'])

    # print(info, links, reputation, sep='\n')
