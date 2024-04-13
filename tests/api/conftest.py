import pytest

from api.models import Profile


@pytest.fixture
def profile_name_instance():
    return Profile.objects.create(column_name="name")


@pytest.fixture
def profile_title_instance():
    return Profile.objects.create(column_name="title", is_visible=False)


@pytest.fixture
def profile_author_instance():
    return Profile.objects.create(column_name="author")
