from api.serializers import ProfileSerializer


def update_profile(profile, data):
    serializer = ProfileSerializer(profile, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
