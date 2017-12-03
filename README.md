# Asudo Vitalik
Intelligent Agent for Blockchain Investors

## Aim
Asudo Vitalik is an Intelligent Agent for[OWN](https://own.space)platform 
that helps investors and traiders to analyse 
Ethereum based tokens and ICOs. 


## Dependencies
To run Asudo Vitalik you need to install following software:
1. python and python-devel (tested with version 3.5)
2. etherscan library from[repository](https://github.com/corpetty/py-etherscan-api)


## Deploy
To deploy Asudo Vitalik you should pass through several steps:
1. Run a WidgetServer from ```OWN_ICO_Widgets/OWN_ICO_Widgets.py``` module  

2. Configure Agent
Most of setting provided in ```agents_platform/settings.py```  
    1. You should provide credentials with AGENT_LOGIN and AGENT_PASSWORD variables.  
    2. Then you should provide url of your WidgetServer with WIDGET_SERVER_URL variable.
    3. Also you should provide path to folder for storing logs with LOGS_DIRECTORY_PATH variable.

3. Run an Agent
Now you can start an agent service by running
    ````
    $ python agents_platform/hello_world_agent.py
    ````

## Using an Agent
After starting an agent service you need to complete two steps:
1. Add Agent to a clean board
2. Create an element on X=1, Y=1 with following caption:
```@helloworld:<ICO company/Token name>```

Now you can go and take a cup of tea: 
Vitalik needs several minutes to make his analysis for you.