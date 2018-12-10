import pytest

from services import UserStoryParser
from exceptions import InvalidTrelloCardName


def test_is_user_story_return_false():
    card_description = '''
        # Cheerios
        Given i like to boogie
        When someone plays boogie
        Then i start dancing

        Given I love candy
        when someone gives my candy
        then i say thank you
    '''

    result = UserStoryParser().is_user_story(card_description)

    assert result is False


def test_is_user_story_return_true():
    card_description = '''
        # Scenarios
        Given i like to boogie
        When someone plays boogie
        Then i start dancing

        Given I love candy
        when someone gives my candy
        then i say thank you
    '''

    result = UserStoryParser().is_user_story(card_description)

    assert result is True


def test_get_feature():
    card = {
        'id': 'myid',
        'name': '[users]My nice feature',
        'desc': '''
            my little description

            # Scenarios
            Given i like to boogie
            When someone plays boogie
            Then i start dancing

            Given I love candy
            when someone gives my candy
            then i say thank you
        '''
    }

    result = UserStoryParser().get_feature(card)

    assert result == 'My nice feature'


def test_get_filename():
    card = {
        'id': 'myid',
        'name': '[users] My nice feature'
    }

    result = UserStoryParser().get_file_name(card)

    assert result == 'users'


def test_get_filename_exception():
    card = {
        'id': 'myid',
        'name': 'My nice feature'
    }

    with pytest.raises(InvalidTrelloCardName):
        UserStoryParser().get_file_name(card)


def test_get_filename_empty():
    card = {
        'id': 'myid',
        'name': ' [] My nice feature'
    }

    with pytest.raises(InvalidTrelloCardName):
        UserStoryParser().get_file_name(card)


def test_get_filename_space():
    card = {
        'id': 'myid',
        'name': ' [users] My nice feature'
    }

    result = UserStoryParser().get_file_name(card)

    assert result == 'users'


def test_get_filename_empty_brackets():
    card = {
        'id': 'myid',
        'name': '[] My nice feature'
    }

    with pytest.raises(InvalidTrelloCardName):
        UserStoryParser().get_file_name(card)


def test_get_tag_only_return_trello_tag():
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''
            my little description

            # Scenarios
            Given i like to boogie
            When someone plays boogie
            Then i start dancing

            Given I love candy
            when someone gives my candy
            then i say thank you
        ''',
        'due': ''
    }

    result = UserStoryParser().get_tags(card)

    assert '@trello-{id}'.format(id=card['id']) in result


def test_get_tag_return_all_tags():
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''
            my little description

            # Scenarios
            Given i like to boogie
            When someone plays boogie
            Then i start dancing

            Given I love candy
            when someone gives my candy
            then i say thank you
        ''',
        'due': '2018-12-04'
    }

    result = UserStoryParser().get_tags(card)

    assert '@trello-{id}'.format(id=card['id']) in result and '@release-{due}'.format(due=card['due']) in result


def test_get_description_when_is_empty():
    expected_result = ''
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''

            # Scenarios
            Given i like to boogie
            When someone plays boogie
            Then i start dancing

            Given I love candy
            when someone gives my candy
            then i say thank you
        '''
    }

    result = UserStoryParser().get_description(card)

    assert result == expected_result


def test_get_description_when_not_empty():
    expected_result = 'my little description'
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''
            my little description

            # Scenarios
            Given i like to boogie
            When someone plays boogie
            Then i start dancing

            Given I love candy
            when someone gives my candy
            then i say thank you
        '''
    }

    result = UserStoryParser().get_description(card)

    assert result == expected_result


def test_get_scenarios_when_empty():
    expected_result = []
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''
            my little description

            # Scenarios


        '''
    }

    result = UserStoryParser().get_scenarios(card)

    assert result == expected_result


def test_get_scenarios_when_one_scenario_present():
    expected_result = [
        [
            'Given I love candy',
            'when someone gives my candy',
            'then i say thank you'
        ]
    ]
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''
            my little description

            # Scenarios

            Given I love candy
            when someone gives my candy
            then i say thank you

        '''
    }

    result = UserStoryParser().get_scenarios(card)

    assert result == expected_result


def test_get_scenarios_when_more_than_one_scenario_present():
    expected_result = [
        [
            'Given i like to boogie',
            'When someone plays boogie',
            'Then i start dancing'
        ],
        [
            'Given I love candy',
            'when someone gives my candy',
            'then i say thank you'
        ]
    ]
    card = {
        'id': 'myid',
        'name': '[users] My nice feature',
        'desc': '''
            my little description

            # Scenarios
            Given i like to boogie
            When someone plays boogie
            Then i start dancing

            Given I love candy
            when someone gives my candy
            then i say thank you

        '''
    }

    result = UserStoryParser().get_scenarios(card)

    assert result == expected_result


def test_get_scenario_empty_story():
    expected_result = []
    scenario = '''

    '''

    result = UserStoryParser().get_scenario(scenario)

    assert result == expected_result


def test_scenario_with_newlines():
    expected_result = [
        'Given I love candy',
        'when someone gives my candy',
        'then i say thank you'
    ]
    scenario = '''
        Given I love candy

        when someone gives my candy
        then i say thank you


    '''

    result = UserStoryParser().get_scenario(scenario)

    assert result == expected_result


def test_scenario_with_no_newlines():
    expected_result = [
        'Given I love candy',
        'when someone gives my candy',
        'then i say thank you'
    ]
    scenario = '''
        Given I love candy
        when someone gives my candy
        then i say thank you
    '''

    result = UserStoryParser().get_scenario(scenario)

    assert result == expected_result
