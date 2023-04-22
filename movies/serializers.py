from rest_framework import serializers
from .models import Movie, Rating


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(
        max_length=10, allow_null=True, default=None
    )
    rating = serializers.ChoiceField(
        choices=Rating.choices, default=Rating.GENERAL_AUDIENCES
    )
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.EmailField(read_only=True, source="user.email")

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
