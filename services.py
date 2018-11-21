import requests


class TrelloClientService():
    def __init__(self, token, app_key, board):
        self.url = 'https://api.trello.com/1/boards/{board}/cards?key={app_key}&token={token}'.format(
            board=board, app_key=app_key, token=token)

    def get_cards(self):
        res = requests.get(self.url)
        return res.json()


class UserStoryService():
    SCENARIO_START = '# Scenarios'

    def process_cards(self, cards):
        cards = [
            dict(id=item['id'], desc=item['desc'], name=item['name'])
            for item in cards
        ]

        for card in cards:
            if not self.is_user_story(card):
                continue

            else:
                user_story = self.get_user_story(card)
                self.save_user_story(user_story)

    def is_user_story(self, card):
        return self.SCENARIO_START in card['desc']

    def get_user_story(self, card):
        scenarios_start_index = card['desc'].find(self.SCENARIO_START) + len(self.SCENARIO_START)

        print('Feature: {}\n'.format(card['name']))
        print('  {}\n\n'.format(
            card['desc'][:scenarios_start_index - len(self.SCENARIO_START)].strip()))

        scenarios = card['desc'][scenarios_start_index:]

        for scenario in scenarios.split('--'):
            print('\n  @trello-{}'.format(card['id']))

            for sentence in scenario.split('\n'):
                new_sentence = sentence.strip()

                if not new_sentence:
                    continue

                print('  {}'.format(new_sentence))

    def save_user_story(self, card):
        print('Saved!')