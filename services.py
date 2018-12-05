import requests
import string
import os
import re
from os import listdir
from os.path import isfile, join

from pathlib import Path

from exceptions import InvalidTrelloCardName


class TrelloClientService():
    def __init__(self, token, app_key):
        self.credentials = {"key": app_key, "token": token}

    def get_cards(self, board_id):
        url = self.generate_url('boards', board_id, 'cards')
        return self.perform_request('GET', url, self.credentials)

    def update_card(self, card_id, data):
        url = self.generate_url('cards', card_id, '')
        data.update(self.credentials)
        return self.perform_request('PUT', url, data)

    def generate_url(self, resource, id, item=None):
        return "https://api.trello.com/1/{resource}/{id}/{item}".format(
            resource=resource, item=item, id=id)

    def perform_request(self, method, url, params):
        res = requests.request(method, url, params=params)
        res.raise_for_status()
        return res.json()


class TrelloCardSerializer():
    TAG_REGEXP = r'\@trello-([0-9a-z]+)'

    def get_user_stories_as_cards(self, features_from_files):
        return map(
            lambda key, value: self.get_feature_as_card(key, value),
            features_from_files.keys(), features_from_files.values()
        )

    def get_feature_as_card(self, key, item)-> dict:
        card = {
            'id': self.get_id(item),
            'name': self.get_name(key, item),
            'desc': self.get_desc(item)
        }
        return card

    def feature_to_array(self, feature):
        return [feature for feature in feature.split("\n") if feature.strip()]

    def get_id(self, item):
        feature = self.feature_to_array(item)
        index = 1
        if self.description_exists(feature):
            index = 2
        return feature[index].strip().split('-')[1]

    def get_file_name(self, key):
        feature = self.feature_to_array(key)
        file_name = feature[0].split('.')[0]
        return file_name

    def get_name(self, key, item):
        feature = self.feature_to_array(item)
        item_feature = feature[0].split(':')[1].strip()
        name = "[{}] {}".format(self.get_file_name(key), item_feature)
        return name

    def description_exists(self, feature):
        if not re.match(self.TAG_REGEXP, feature[1].strip()):
            return True
        return False

    def get_desc(self, item):
        feature = self.feature_to_array(item)
        SCENARIO_START = '\n\n# Scenarios\n'
        SCENARIO_SEPARATOR = '--'
        init_index = 3
        desc = ''

        if self.description_exists(feature):
            desc += feature[1].strip()
            init_index = 4

        desc += SCENARIO_START

        for index in range(init_index, len(feature)):
            desc += "{} {}".format(feature[index].strip(), '\n')

        return desc.replace('Scenario:', SCENARIO_SEPARATOR)


class UserStoryParser():
    SCENARIO_START = '# Scenarios'
    SCENARIO_SEPARATOR = '--'
    TRELLO_TAG_FORMAT = '@trello-{}'
    RELEASE_TAG_FORMAT = '@release-{}'

    def get_cards_as_user_stories(self, cards: dict) -> list:
        user_story_cards = filter(
            lambda card: self.is_user_story(card['desc']),
            cards)

        return map(
            lambda card: self.get_user_story(card),
            user_story_cards
        )

    def get_relevant_card_info(self, cards: list) -> dict:
        return [
            dict(id=item['id'], desc=item['desc'], name=item['name'], due=self.parse_date_string(item['due']))
            for item in cards
        ]

    def is_user_story(self, description: str) -> bool:
        return self.SCENARIO_START in description

    def get_user_story(self, card: dict) -> dict:
        user_story = {
            'feature': self.get_feature(card),
            'scenarios': self.get_scenarios(card),
            'tags': self.get_tags(card),
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

    def get_tags(self, card: dict) -> list:
        tags = []
        tags.append(self.TRELLO_TAG_FORMAT.format(card['id']))

        if card['due']:
            tags.append(self.RELEASE_TAG_FORMAT.format(card['due']))

        return tags

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

    def parse_date_string(self, string_date: str) -> str:
        if not string_date:
            return None

        return string_date[:10]

class PersistUserStoryService:
    def save(self, cards, output_path):
        self.create_dir(output_path)
        for card in cards:
            self.save_file(card, output_path)

    def save_file(self, card, output_path):
        filename = '{}.feature'.format(card['file_name'])
        filepath = Path(output_path) / filename

        with open(filepath, 'w') as file_to_be_saved:
            file_content = self.generate_file_content(card)
            file_to_be_saved.write(file_content)

    def create_dir(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            return output_path

    def get_features_from_files(self, output_path):
        files = [file for file in listdir(output_path) if isfile(join(
            output_path, file))]
        features = {}

        for file in files:
            with open(Path(output_path) / file, 'r') as file_to_be_read:
                features[file] = file_to_be_read.read()
        return features

    def generate_file_content(self, card):
        template = '''
            Feature: {feature}

            {description}

{tags_formatted}

{scenarios_formatted}

        '''
        scenarios_formatted = self.format_scenarios(card['scenarios'])
        tags_formatted = self.format_tags(card['tags'])

        return template.format(**card, tags_formatted=tags_formatted, scenarios_formatted=scenarios_formatted)

    def format_scenarios(self, scenarios):
        SEPARATION_FORMAT = '\n{spaces}'.format(spaces=' ' * 14)
        scenarios_formatted = ''

        for scenario in scenarios:
            scenarios_formatted += SEPARATION_FORMAT + 'Scenario:\n'
            scenarios_formatted += SEPARATION_FORMAT
            scenarios_formatted += SEPARATION_FORMAT.join(scenario)
            scenarios_formatted += '\n'

        return scenarios_formatted

    def format_tags(self, tags):
        TAG_SEPARATION_FORMAT = '\n{spaces}'.format(spaces=' ' * 12)
        tags_formatted = ''

        for tag in tags:
            tags_formatted += TAG_SEPARATION_FORMAT + tag

        return tags_formatted
