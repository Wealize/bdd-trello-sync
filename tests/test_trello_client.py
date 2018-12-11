import os

import pytest
import responses
from dotenv import load_dotenv

from services import TrelloClientService

APP_ROOT = os.path.join(os.path.dirname(__file__), '../')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


@responses.activate
def test_create_card_return_card():
    host = 'https://api.trello.com/1/cards'
    token = 'token'
    app_key = 'app_key'
    id_list = 'myid'
    data = {"name": "name", "desc": "desc", "idList": id_list}
    responses.add(
        responses.POST,
        host,
        json=data,
        status=200)
    trello_client_service = TrelloClientService(token, app_key)
    querystring = {"name": "name", "desc": "desc", "idList": id_list}

    response = trello_client_service.create_card(querystring)

    assert response == data


@responses.activate
def test_update_card_return_card():
    url_generated = 'https://api.trello.com/1/cards/mycard?name=name&key=key&token=token'
    token = 'token'
    app_key = 'key'
    card_id = 'mycard'
    data = {"name": "name", "desc": "desc"}
    responses.add(
        responses.PUT,
        url_generated,
        json=data,
        status=200)
    querystring = {"name": "name"}
    trello_client_service = TrelloClientService(token, app_key)

    response = trello_client_service.update_card(card_id, querystring)

    assert response == data


def test_generate_url_when_receive_all_params():
    trello_client_service = TrelloClientService('', '')
    expected_result = 'https://api.trello.com/1/boards/1234/cards'

    result = trello_client_service.generate_url('boards', '1234', 'cards')

    assert result == expected_result


def test_generate_url_when_receive_two_params():
    trello_client_service = TrelloClientService('', '')
    expected_result = 'https://api.trello.com/1/cards/1234/'

    result = trello_client_service.generate_url('cards', '1234')

    assert result == expected_result
