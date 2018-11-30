import requests
import string
import os
import re
from os import listdir
from os.path import isfile, join

from pathlib import Path

from exceptions import InvalidTrelloCardName



class TrelloClientService():
    def __init__(self, token, app_key, board):
        self.url = 'https://api.trello.com/1/boards/{board}/cards?key={app_key}&token={token}'.format(
            board=board, app_key=app_key, token=token)

    def get_cards(self):
        res = requests.get(self.url)
        res.raise_for_status()
        return res.json()

    def update_board(self, features):
        # for f in features: updateCard(f)
        print('')

    def update_card(self, feature):
        # put to Trello Api
        print('')


class TrelloCardSerializer():
    def get_user_stories_as_cards(self, features_from_files):
        return features_from_files

    def get_feature_as_card(self, feature)-> dict:
        card = {
            'id': self.get_id(feature),
            'name': self.get_name(feature),
            'desc': self.get_desc(feature)
        }
        return card

    def feature_to_array(self, feature):
        return list(filter(None, feature.split("\n")))

    def get_id(self, feature):
        if self.description_exists(feature):
            return feature[3].split('-')[1]
        return feature[2].split('-')[1]

    def get_file_name(self, feature):
        file_name = feature[0].split('.')[0]
        return '[{}]'.format(file_name)

    def get_name(self, feature):
        item_feature = feature[1].split(':')[1].strip()
        name = "{} {}".format(self.get_file_name(feature), item_feature)
        return name

    def description_exists(self, feature):
        if re.match(r'\@trello-([0-9a-z]+)', feature[2].strip()) == None:
            return True
        return False

    def get_desc(self, feature):
        SCENARIO_START = '# Scenarios'
        SCENARIO_SEPARATOR = '--'




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
        self.create_dir(output_path)
        for card in cards:
            self.save_file(card, output_path)

    def save_file(self, card, output_path):
        filename = '{}.feature'.format(card['file_name'])
        filepath = Path(output_path) / filename

        with open(filepath, 'w') as file_tobe_saved:
            file_content = self.generate_file_content(card)
            file_tobe_saved.write(file_content)

    def create_dir(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            return output_path

    def get_features_from_files(self, output_path):
        files = [f for f in listdir(output_path) if isfile(join(output_path, f))]
        features = []

        for f in files:
            with open( Path(output_path) / f, 'r') as file_tobe_read:
                features.append(f + ':' + str(file_tobe_read.read()))
        return features

    def generate_file_content(self, card):
        template = '''
            Feature: {feature}

            {description}

            {tag}

{scenarios_formatted}

        '''
        scenarios_formatted = self.format_scenarios(card['scenarios'])

        return template.format(**card, scenarios_formatted=scenarios_formatted)

    def format_scenarios(self, scenarios):
        SEPARATION_FORMAT = '\n{spaces}'.format(spaces=' ' * 14)
        scenarios_formatted = ''

        for scenario in scenarios:
            scenarios_formatted += SEPARATION_FORMAT + 'Scenario:\n'
            scenarios_formatted += SEPARATION_FORMAT
            scenarios_formatted += SEPARATION_FORMAT.join(scenario)
            scenarios_formatted += '\n'

        return scenarios_formatted
