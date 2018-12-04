import pytest

from services import TrelloCardSerializer


def test_get_id_when_receive_params():
    item = '''\nFeature:  example\n\nSmall description\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n'''
    serializer = TrelloCardSerializer()
    expected_result = '1234'

    result = serializer.get_id(item)

    assert result == expected_result


def test_get_id_when_params_is_empty():
    item = ''
    serializer = TrelloCardSerializer()

    with pytest.raises(IndexError):
        serializer.get_id(item)


def test_get_file_name_when_receive_params():
    key = 'candy.feature'
    serializer = TrelloCardSerializer()
    expected_result = '[candy]'

    result = serializer.get_file_name(key)

    assert result == expected_result


def test_get_file_name_when_params_is_empty():
    key = ''
    serializer = TrelloCardSerializer()

    with pytest.raises(IndexError):
        serializer.get_file_name(key)


def test_get_name_when_receive_params():
    key = 'candy.feature'
    item = '''\nFeature:  example\n\nSmall description\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n'''
    serializer = TrelloCardSerializer()
    expected_result = '[candy] example'

    result = serializer.get_name(key, item)

    assert result == expected_result


def test_get_name_when_params_is_empty():
    key = ''
    item = ''
    serializer = TrelloCardSerializer()

    with pytest.raises(IndexError):
        serializer.get_name(key, item)


def test_description_exists_is_true_when_description_exists():
    serializer = TrelloCardSerializer()
    item = serializer.feature_to_array('''\nFeature:  example\n\nSmall description\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n''')
    expected_result = True

    result = serializer.description_exists(item)

    assert result == expected_result


def test_description_exists_is_false_when_description_not_exists():
    serializer = TrelloCardSerializer()
    item = serializer.feature_to_array('''\nFeature:  example\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n''')
    expected_result = False

    result = serializer.description_exists(item)

    assert result == expected_result


def test_description_exists_raise_exception_when_params_is_empty():
    item = ''
    serializer = TrelloCardSerializer()

    with pytest.raises(IndexError):
        serializer.description_exists(item)


def test_get_desc_when_receive_params():
    item = '''\nFeature:  example\n\nSmall description\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n'''
    expected_result = 'Small description\n\n# Scenarios\nGiven i like to \nboogie \n'
    serializer = TrelloCardSerializer()

    result = serializer.get_desc(item)

    assert result == expected_result


def test_get_desc_when_params_is_empty():
    item = ''
    serializer = TrelloCardSerializer()

    with pytest.raises(IndexError):
        serializer.get_desc(item)


def test_feature_to_array_when_receive_params():
    item = '''\nFeature:  example\n\nSmall description\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n'''
    serializer = TrelloCardSerializer()
    expected_result = ['Feature:  example', 'Small description']
    expected_result.extend(['        @trello-1234', '  Scenario:'])
    expected_result.extend(['  Given i like to', '        boogie'])

    result = serializer.feature_to_array(item)

    assert result == expected_result


def test_feature_to_array_when_param_is_empty():
    item = ''
    serializer = TrelloCardSerializer()
    expected_result = []

    result = serializer.feature_to_array(item)

    assert result == expected_result


def test_get_feature_as_card_if_key_item_is_given():
    key = 'candy.feature'
    item = '''\nFeature:  example\n\nSmall description\n\n
        @trello-1234\n\n\n  Scenario:\n\n  Given i like to
        boogie\n\n\n'''
    serializer = TrelloCardSerializer()
    desc = 'Small description\n\n# Scenarios\nGiven i like to \nboogie \n'
    expected_result = {'desc': desc, 'id': '1234', 'name': '[candy] example'}

    result = serializer.get_feature_as_card(key, item)

    assert result == expected_result


def test_get_feature_as_card_when_params_is_empty():
    key = ''
    item = ''
    serializer = TrelloCardSerializer()

    with pytest.raises(IndexError):
                serializer.get_feature_as_card(key, item)
