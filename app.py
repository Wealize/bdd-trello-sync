import os

import click

from services import TrelloClientService, UserStoryService

@click.command()
@click.option('--action', type=click.Choice(['sync', 'update']), help='action to execute')

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
    user_story_service = UserStoryService()
    cards = user_story_service.process_cards(client_service.get_cards())

def update():
    print('TO DO update')

if __name__ == '__main__':
    main()