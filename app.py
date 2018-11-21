import os

from services import TrelloClientService, UserStoryService


def main():
    token = os.environ.get('TRELLO_TOKEN')
    app_key = os.environ.get('TRELLO_APP_KEY')
    board = os.environ.get('TRELLO_BOARD')
    client_service = TrelloClientService(token, app_key, board)
    user_story_service = UserStoryService()
    cards = user_story_service.process_cards(client_service.get_cards())


if __name__ == '__main__':
    main()