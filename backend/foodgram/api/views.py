from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet


from recipes.models import Tag, Recipe
from api.serialiazers import TagSerializer, RecipeSerializer

# Create your views here.
class CustomUserViewset(UserViewSet):
    pass

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    