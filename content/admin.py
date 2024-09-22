from django.contrib import admin
from .models import Content, Poem, Story, Information, Question, Perception, Comment 

# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["created_at", "updated_at"]


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    # list_display = [
    #     "title",
    #     "body",
    # ]
    pass


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    # list_display = ["title", "body"]
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # list_display = ["topic", "questions"]
    pass


@admin.register(Perception)
class PerceptionAdmin(admin.ModelAdmin):
    # list_display = ["topic", "thought"]
    pass


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    # list_display = ["topic", "informations"]
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "parent"]
