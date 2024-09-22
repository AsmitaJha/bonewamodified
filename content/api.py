import datetime
import random
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import filters, generics, mixins, response, status, viewsets
from django.http import HttpResponse
from django.utils import timezone
from .serializers import (
    CommentSerializer,
    ContentSerializer,
    InformationSerializer,
    PerceptionSerializer,
    PoemSerializer,
    QuestionSerializer,
    StorySerializer,
)
from .models import Comment


class ContentCreateView(viewsets.ModelViewSet):
    # queryset = Content.Objects.all()
    # serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    serializer_mapping = {
        "Poem": PoemSerializer,
        "Story": StorySerializer,
        "Question": QuestionSerializer,
        "Perception": PerceptionSerializer,
        "Information": InformationSerializer,
    }

    def get_serializer_class(self,content_type):
        serializer_class = self.serializer_mapping.get(content_type)
        if serializer_class is None:
            raise ValidationError("Invalid content type. Please enter a valid one.")

        return serializer_class
        # return ValueError("You have provided an invalid content type. Please provide a valid one. ")

    def create(self, request, *args, **kwargs):
       
        content_type=request.query_params.get("content_type")
        serializer_class = self.get_serializer_class(content_type)
        serializer = serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, AllowAny]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
