import os

import click
from dotenv import load_dotenv

from services import TrelloClientService, UserStoryParser, PersistUserStoryService, TrelloCardSerializer
APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

@click.command()
@click.option('--board', required=True, help='board of project')
@click.option('--path', required=True, help='output path')
@click.option('--push', is_flag=True, help='push from Behave to Trello. Without this option pull Trello to Behave')


def main(board, path, push):
    token = os.getenv('TRELLO_TOKEN')
    app_key = os.getenv('TRELLO_APP_KEY')
    client_service = TrelloClientService(token, app_key, board)
    if push:
        sync_from_behave_to_trello(client_service, path)
    else:
        sync_from_trello_to_behave(client_service, path)


def sync_from_trello_to_behave(client_service, path):
    parser = UserStoryParser()
    cards = parser.get_cards_as_user_stories(client_service.get_cards())
    persit_service = PersistUserStoryService()
    persit_service.save(cards, path)


def sync_from_behave_to_trello(client_service, path):
    # TODO

if __name__ == '__main__':
    main()