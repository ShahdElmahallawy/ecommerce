from api.models import Profile


def get_user_profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return None
    return profile
