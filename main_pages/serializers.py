from rest_framework import serializers
from main_pages.models import Rating
class ScoreSerializer (serializers.ModelSerializer ):
    class Meta:
        model = Rating
        fields = "__all__"