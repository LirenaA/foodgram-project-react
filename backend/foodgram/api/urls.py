from rest_framework import routers
from django.urls import path, include
from djoser import views as djoser_views

from users.views import CustomUserViewset
from api.views import TagViewSet, RecipeViewSet, IngredientViewSet


router = routers.DefaultRouter()
router.register('users', CustomUserViewset)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
]


