import pytest
from django.contrib.auth import get_user_model
from api.models import Profile
from api.selectors import get_user_profile

User = get_user_model()


@pytest.mark.django_db
def test_get_user_profile(user):
    profile = Profile.objects.get(user=user)

    retrieved_profile = get_user_profile(user)

    assert retrieved_profile == profile
    assert retrieved_profile.user == user


@pytest.mark.django_db
def test_get_user_profile_fail(user):

    profile = Profile.objects.get(user=user)
    profile.delete()

    retrieved_profile = get_user_profile(user)

    assert retrieved_profile == None
