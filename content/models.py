from django.db import models
from user.models import User
from django.utils import timezone

class Content(models.Model):
    # content_type = models.ChoiceField(choices=content_choices)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="content", null=True, blank=True
    )
    # many to one or one to many

    # class Meta:
    # abstract=True


class Poem(Content):
    thumbnail = models.ImageField(upload_to="images/poem/", null=True, blank=True)


class Story(Content):
    thumbnail = models.ImageField(upload_to="images/story/", null=True, blank=True)


class Question(Content):
    thumbnail = models.ImageField(upload_to="images/question/", null=True, blank=True)


class Perception(Content):
    pass


class Information(Content):
    thumbnail = models.ImageField(
        upload_to="information_related_pics/", null=True, blank=True
    )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.TextField()
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="thread_comment"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

