from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


from recipes.models import Tag, Recipe, Ingredient
from api.serialiazers import TagSerializer, RecipeSerializer, RecipeCreateSerializer, IngredientSerializer

# Create your views here.
class CustomUserViewset(UserViewSet):
    pass

class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer
    
class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()