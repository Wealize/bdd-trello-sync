import pytest

from services import PersistUserStoryService


def test_format_scenarios_when_receive_scenarios_return_scenarios_formatted():
        persistservice = PersistUserStoryService()
        scenarios = [['aaa', 'bbb']]
        scenarios_formatted = '''
              Scenario:

              aaa
              bbb
'''

        result = persistservice.format_scenarios(scenarios)

        assert result == scenarios_formatted


def test_format_scenarios_when_no_receive_scenarios_return_empty_string():
        persistservice = PersistUserStoryService()
        scenarios = []

        result = persistservice.format_scenarios(scenarios)

        assert result == ''


def test_generate_file_content_when_receive_card_return_feature_formatted():
        persistservice = PersistUserStoryService()
        card = {
        'feature':
                'My little description',
                'scenarios': [
                        [
                                'Given I love candy',
                                'when someone gives me candy'
                        ]
                ],
                'tag': '@trello-5bf52341087e6a847a624604',
                'description': 'Small description of the feature',
                'file_name': 'users'
        }

        expected_result = '''
            Feature: My little description

            Small description of the feature

            @trello-5bf52341087e6a847a624604


              Scenario:

              Given I love candy
              when someone gives me candy


        '''

        result = persistservice.generate_file_content(card)

        assert result == expected_result


def test_generate_file_content_when_no_receive_card_return_feature_formatted():
        persistservice = PersistUserStoryService()
        card = {}

        with pytest.raises(KeyError):
                persistservice.generate_file_content(card)

@pytest.fixture
def test_create_dir_when_directory_not_exists(tempfile):
        persistservice = PersistUserStoryService()
        directory = tempfile('feature')

        result = persistservice.create_dir(directory)

        assert result == 'feature'

def test_create_dir_when_directory_exists(tmpdir):
        persistservice = PersistUserStoryService()
        directory = tmpdir.mkdir('feature')

        result = persistservice.create_dir(directory)

        assert result == None