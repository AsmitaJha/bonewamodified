from rest_framework import serializers
from content.models import Story, Poem, Content, Information, Comment, Question, Perception

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = "__all__"


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class PerceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perception
        fields = "__all__"


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    # content = serializers.PrimaryKeyRelatedField(read_only=True)
    # content_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
