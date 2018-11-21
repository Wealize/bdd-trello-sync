from services import UserStoryService

def test_is_user_story_return_false():
    card_description = '''
        # Cheerios
        Given i like to boogie
        When someone plays boogie
        Then i start dancing

        --

        Given I love candy
        when someone gives my candy
        then i say thank you
    '''

    result = UserStoryService().is_user_story(card_description)

    assert result is False

def test_is_user_story_return_true():
    card_description = '''
        # Scenarios
        Given i like to boogie
        When someone plays boogie
        Then i start dancing

        --

        Given I love candy
        when someone gives my candy
        then i say thank you
    '''

    result = UserStoryService().is_user_story(card_description)

    assert result is True