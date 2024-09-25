from rest_framework import serializers


def only_characters(value):
    """Validate that the value contains only characters."""
    if not all(char.isalpha() or char.isspace() for char in value):
        raise serializers.ValidationError("Only characters are allowed.")
    return value


def only_alphanumeric(value):
    """Validate that the value contains only alphanumeric characters."""
    if not all(char.isalnum() or char.isspace() for char in value):
        raise serializers.ValidationError("Only alphanumeric characters are allowed.")
    return value


def only_digits(value):
    """Validate that the value contains only digits."""
    if not value.isdigit():
        raise serializers.ValidationError("Only digits are allowed.")
    return value
