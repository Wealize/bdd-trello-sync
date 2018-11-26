import os

import click
from dotenv import load_dotenv

from services import TrelloClientService, UserStoryParser, PersistUserStoryService

APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

@click.command()
@click.option('--board', required=True, help='board of project')
@click.option('--path', required=True, help='output path')

def main(board, path):
    token = os.getenv('TRELLO_TOKEN')
    app_key = os.getenv('TRELLO_APP_KEY')
    client_service = TrelloClientService(token, app_key, board)
    parser = UserStoryParser()
    cards = parser.get_cards_as_user_stories(client_service.get_cards())
    persit_service = PersistUserStoryService()
    persit_service.save(cards, path)

if __name__ == '__main__':
    main()