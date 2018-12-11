import os

import click
from dotenv import load_dotenv

from services import TrelloClientService, UserStoryParser, PersistUserStoryService, TrelloCardSerializer
APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

VALID_TRELLO_CARD_KEYS = {'name', 'desc'}

@click.command()
@click.option('--board', required=True, help='board of project')
@click.option('--path', required=True, help='output path')
@click.option('--push', is_flag=True, help='push from Behave to Trello. Without this option pull Trello to Behave')

def main(board, path, push):
    token = os.getenv('TRELLO_TOKEN')
    app_key = os.getenv('TRELLO_APP_KEY')
    client_service = TrelloClientService(token, app_key)
    if push:
        sync_from_behave_to_trello(client_service, path, board)
    else:
        sync_from_trello_to_behave(client_service, path, board)


def sync_from_trello_to_behave(client_service, path, board):
    parser = UserStoryParser()
    cards = parser.get_cards_as_user_stories(client_service.get_cards(board))
    persit_service = PersistUserStoryService()
    persit_service.save(cards, path)


def sync_from_behave_to_trello(client_service, path, board):
    persit_service = PersistUserStoryService()
    card_serializer = TrelloCardSerializer()
    cards = card_serializer.get_user_stories_as_cards(
        persit_service.get_features_from_files(path))
    id_list = client_service.get_id_first_list(board)
    for card in cards:
        push_card(card, id_list, client_service)

def push_card(card, id_list, client_service):
    data = {key: value for key, value in card.items() if
            key in VALID_TRELLO_CARD_KEYS}
    card_id = card.get('id', None)
    if not card_id:
        data.update({"idList": id_list})
        client_service.create_card(data)
    else:
        client_service.update_card(card_id, data)

if __name__ == '__main__':
    main()