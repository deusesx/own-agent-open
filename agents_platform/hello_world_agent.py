import json
import re
import threading
import time
import traceback
import urllib

import websocket

import logger
from own_adapter.agent import Agent
from own_adapter.board import Board
from own_adapter.element import Element
from own_adapter.platform_access import PlatformAccess
from settings import WIDGET_SERVER_URL
from settings import EMBEDDING_URL


AGENT_LOGIN = 'samigullin.art@gmail.com'
AGENT_PASSWORD = 'deusdeus'


def __do_something(element, **kwargs):
    """Write your code here"""
    token_name=kwargs.get('token_name', None)
    if token_name is None:
        raise Exception()

    message = 'Searching data about {}'.format(token_name)
    board = element.get_board()
    board.put_message(message)

    w1 = board.add_element(2,1,6,3, 'Company profile')
    w2 = board.add_element(1,4,5,2, 'ICO activity')
    w3 = board.add_element(1,6,4,2, 'Current projects activity')
    w4 = board.add_element(5,6,3,2, 'One more widget')

    __add_widget(w1, token_name)
    __add_widget(w2, token_name, 'diagram')
    __add_widget(w3, token_name, 'ico_widget')


def __add_widget(element, token_name, w_type="token_profile"):
    # put a URL to an element
    params = urllib.parse.urlencode({'token_name': token_name})
    widget_url = "{0}/{2}/?{1}".format(
        WIDGET_SERVER_URL, params, w_type)
    url = "{0}{1}".format(EMBEDDING_URL, widget_url)
    element.put_link(url)


def __run_on_element(element, **kwargs):
    """Running on a target element"""
    try:
        __do_something(element, **kwargs)
    except Exception as ex:
        logger.exception('helloworld', 'Error: could not process an element. Element id: {}. Exception message: {}.\n'
                                       '{}'.format(element.get_id(), str(ex), traceback.format_exc()))


def __run_on_board(board):
    """Runs the agent on elements of a board"""
    elements = board.get_elements()
    for element in elements:
        __run_on_element(element)


def periodical_update():
    """Does periodical work with a predefined time interval"""
    time_interval = 86400

    while True:
        time.sleep(time_interval)

        agent = get_agent()
        boards = agent.get_boards()
        for board in boards:
            __run_on_board(board)
        logger.info('helloworld', 'Daily news update is done.')


def get_agent():
    """Returns the current agent"""
    login = AGENT_LOGIN
    password = AGENT_PASSWORD

    platform_access = PlatformAccess(login, password)
    helloworld_agent = Agent(platform_access)

    return helloworld_agent


def on_websocket_message(ws, message):
    """Processes websocket messages"""
    message_dict = json.loads(message)
    content_type = message_dict['contentType']
    message_type = content_type.replace('application/vnd.uberblik.', '')

    logger.debug('helloworld', message)

    if message_type == 'liveUpdateElementCaptionEdited+json':
        element_caption = message_dict['newCaption']
        # looking for elements that target our agent
        if re.match(pattern='@helloworld:.+', string=element_caption):
            # create instances of Board and Element to work with them
            element_id = message_dict['path']
            news_agent = get_agent()
            board_id = '/'.join(element_id.split('/')[:-2])
            board = Board.get_board_by_id(board_id, news_agent.get_platform_access(), need_name=False)
            element = Element.get_element_by_id(element_id, news_agent.get_platform_access(), board)
            if element is not None:
                name = element_caption.split(":")[1].strip()
                __run_on_element(element, token_name=name)


def on_websocket_error(ws, error):
    """Logs websocket errors"""
    logger.error('helloworld', error)


def on_websocket_open(ws):
    """Logs websocket openings"""
    logger.info('helloworld', 'Websocket is open')


def on_websocket_close(ws):
    """Logs websocket closings"""
    logger.info('helloworld', 'Websocket is closed')


def open_websocket():
    """Opens a websocket to receive messages from the boards about events"""
    agent = get_agent()
    # getting the service url without protocol name
    platform_url_no_protocol = agent.get_platform_access().get_platform_url().split('://')[1]
    access_token = agent.get_platform_access().get_access_token()
    url = 'ws://{}/opensocket?token={}'.format(platform_url_no_protocol, access_token)

    ws = websocket.WebSocketApp(url,
                                on_message=on_websocket_message,
                                on_error=on_websocket_error,
                                on_open=on_websocket_open,
                                on_close=on_websocket_close)
    ws.run_forever()


def run():
    websocket_thread = None
    updater_thread = None

    while True:
        # opening a websocket for catching server messages
        if websocket_thread is None or not websocket_thread.is_alive():
            try:
                websocket_thread = threading.Thread(target=open_websocket)
                websocket_thread.start()
            except Exception as e:
                logger.exception('helloworld', 'Could not open a websocket. Exception message: {}'.format(str(e)))

        # periodical updates
        if updater_thread is None or not updater_thread.is_alive():
            try:
                updater_thread = threading.Thread(target=periodical_update)
                updater_thread.start()
            except Exception as e:
                logger.exception('helloworld', 'Could not start updater. Exception message: {}'.format(str(e)))

        # wait until next check
        time.sleep(10)


if __name__ == '__main__':
    run()