from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.serializers import UserSerializer
from api.utils import add_ingredients

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriberSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and obj.followed.filter(user=user).exists())

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = int(request.query_params.get('recipes_limit', '5'))
        recipes = obj.recipes.all()[:limit]
        return ShortRecipeSerializer(many=True).to_representation(recipes)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects, source='ingredient.id'
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    amount = serializers.IntegerField(min_value=1, max_value=5000)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='ingredient_amount')
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        return obj.favorites.filter(user=self.context['request'].user).exists()

    def get_is_in_shopping_cart(self, obj):
        return obj.carts.filter(user=self.context['request'].user).exists()


class RecipeCreateSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    cooking_time = serializers.IntegerField(min_value=1, max_value=10000)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient_amount')
        recipe = super().create(validated_data)
        return add_ingredients(recipe, ingredients)

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredient_amount', None)
        recipe = super().update(instance, validated_data)
        if ingredients:
            recipe.ingredients.clear()
            return add_ingredients(recipe, ingredients)
        return recipe
