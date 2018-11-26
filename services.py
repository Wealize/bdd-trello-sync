import requests
import string
from exceptions import InvalidTrelloCardName
import re
from pathlib import Path


class TrelloClientService():
    def __init__(self, token, app_key, board):
        self.url = 'https://api.trello.com/1/boards/{board}/cards?key={app_key}&token={token}'.format(
            board=board, app_key=app_key, token=token)

    def get_cards(self):
        res = requests.get(self.url)
        res.raise_for_status()
        return res.json()


class UserStoryParser():
    SCENARIO_START = '# Scenarios'
    SCENARIO_SEPARATOR = '--'
    TRELLO_TAG_FORMAT = '@trello-{}'

    def get_cards_as_user_stories(self, cards: dict) -> list:
        cards = self.get_relevant_card_info(cards)
        user_story_cards = filter(
            lambda card: self.is_user_story(card['desc']),
            cards)

        return map(
            lambda card: self.get_user_story(card),
            user_story_cards
        )

    def get_relevant_card_info(self, cards: list) -> dict:
        return [
            dict(id=item['id'], desc=item['desc'], name=item['name'])
            for item in cards
        ]

    def is_user_story(self, description: str) -> bool:
        return self.SCENARIO_START in description

    def get_user_story(self, card: dict) -> dict:
        user_story = {
            'feature': self.get_feature(card),
            'scenarios': self.get_scenarios(card),
            'tag': self.get_tag(card),
            'description': self.get_description(card),
            'file_name': self.get_file_name(card)
        }
        return user_story

    def get_feature(self, card: dict) -> str:
        match = re.search(r'\[(\w+)\](.*)', card['name'])

        if match:
            return match.group(2)
        return card['name']

    def get_description(self, card: dict) -> str:
        description = ''

        try:
            description = card['desc'].split(self.SCENARIO_START)[0].strip()
        except IndexError:
            # Empty
            pass

        return description

    def get_tag(self, card: dict) -> str:
        return self.TRELLO_TAG_FORMAT.format(card['id'])

    def get_scenarios(self, card: dict) -> list:
        scenarios = []

        try:
            card_scenarios = card['desc'].split(self.SCENARIO_START)[1].strip()
        except IndexError:
            card_scenarios = []

        for card_scenario in card_scenarios.split(self.SCENARIO_SEPARATOR):
            if not card_scenario.strip():
                continue

            scenarios.append(self.get_scenario(card_scenario))

        return scenarios

    def get_scenario(self, scenario_data):
        scenario = []

        for sentence in scenario_data.split('\n'):
            new_sentence = sentence.strip()

            if not new_sentence:
                continue

            scenario.append(new_sentence)

        return scenario

    def get_file_name(self, card: dict) -> str:

        match = re.search(r'\[(\w+)\]', card['name'])

        if match:
            return match.group(1)
        else:
            raise InvalidTrelloCardName()


class PersistUserStoryService:
    def save(self, cards, output_path):
        for card in cards:
            file_name = card['file_name'] + '.feature'
            path = Path(output_path) / file_name
            open(path, 'w')
            f = open(path, 'a')
            f.write('Feature: ' + card['feature']+'\n\n')
            for scenarios in card['scenarios']:
                f.write('Scenario: ' + card['feature']+'\n')
                for scenario in scenarios:
                    f.write(scenario+'\n')
                f.write('\n')
        f.close()



