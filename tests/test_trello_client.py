import pytest

from services import TrelloClientService


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
