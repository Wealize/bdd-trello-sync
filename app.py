import os

import click

from services import TrelloClientService, UserStoryParser

@click.command()
@click.option('--board', required=True, help='board of project')
@click.option('--path', required=True, help='output path')

def main(board, path):
    token = os.environ.get('TRELLO_TOKEN')
    app_key = os.environ.get('TRELLO_APP_KEY')
    client_service = TrelloClientService(token, app_key, board)
    parser = UserStoryParser()
    cards = parser.get_cards_as_user_stories(client_service.get_cards())
    # TODO Save data from the cards
    for card in cards:
        print(card)

if __name__ == '__main__':
    main()