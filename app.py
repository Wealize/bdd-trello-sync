import os

import click

from services import TrelloClientService, UserStoryParser

ACTIONS = ['sync', 'update']

@click.command()
@click.option('--action', type=click.Choice(ACTIONS), help='action to execute')

def main(action):
    switcher = {
        'sync': sync,
        'update': update
    }
    func = switcher.get(action)
    return func()

def sync():
    token = os.environ.get('TRELLO_TOKEN')
    app_key = os.environ.get('TRELLO_APP_KEY')
    board = os.environ.get('TRELLO_BOARD')
    client_service = TrelloClientService(token, app_key, board)
    parser = UserStoryParser()
    cards = parser.get_cards_as_user_stories(client_service.get_cards())
    # TODO Save data from the cards
    for card in cards:
        print(card)

def update():
    print('TO DO update')

if __name__ == '__main__':
    main()