import pytest

from services import PersistUserStoryService


def test_save_raises_exception():
    user_story = {}

    # Since it's not implemented let's raise an exception for now
    with pytest.raises(NotImplementedError):
        PersistUserStoryService().save(user_story)