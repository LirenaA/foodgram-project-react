from api.filters import RecipeFilter
from api.paginations import PageNumberCustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serialiazers import (IngredientSerializer, RecipeCreateSerializer,
                              RecipeSerializer, ShortRecipeSerializer,
                              TagSerializer)
from api.utils import create_shopping_list
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram import settings
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

User = get_user_model()


# В доке нет фильтрации
class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberCustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)
    ordering = ('-pub_date',)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            Ingredient.objects
            .filter(ingredient_amount__recipe__in_carts=request.user)
            .values('name').annotate(amount=Sum('ingredient_amount__amount'))
            .values('name', 'measurement_unit', 'amount')
        )
        patch = (f'{settings.MEDIA_ROOT}\\send_ingredients\\'
                 f'{request.user.username}_list_of_buy.txt')
        try:
            create_shopping_list(ingredients, patch)
        except (KeyError, IOError) as err:
            return Response({'error': f'Ошибка: {err}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return FileResponse(open(patch, 'rb'), status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=True,
        serializer_class=ShortRecipeSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            if recipe.favorites.filter(user=user).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.recipes_in_favorite.add(recipe)
            return Response(
                data=self.get_serializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        if not recipe.favorites.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.recipes_in_favorite.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        serializer_class=ShortRecipeSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            if recipe.carts.filter(user=user).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.recipes_in_cart.add(recipe)
            return Response(
                data=self.get_serializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        if not recipe.carts.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.recipes_in_cart.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ('^name',)
