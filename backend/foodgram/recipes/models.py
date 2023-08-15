from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя',
    )
    color = ColorField(
        default='#FF0000',
        verbose_name='Цвет'
        )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=False,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name[:50]


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
    )
    cooking_time =  models.PositiveSmallIntegerField(
         validators=[
            MinValueValidator(1),
            MaxValueValidator(10000)
        ],
        verbose_name='Время приготовления')
    text = models.TextField(
        verbose_name='Рецепт приготовления'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/images/'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    # Добавила для удобства добавления в корзину и в избранные
    in_carts = models.ManyToManyField(
        User,
        through='Cart',
        related_name='recipes_in_cart',
        verbose_name='Рецепт в корзине'
    )
    in_favorites = models.ManyToManyField(
        User,
        through='Favorite',
        related_name='recipes_in_favorite',
        verbose_name='Рецепт в избранном'
    )
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
        )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'



class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='ingredient_amount',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
         validators=[
            MinValueValidator(1),
            MaxValueValidator(5000)
        ],
        verbose_name='Количество ингредиента'
    )

    
class UserRecipeAbstract(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Favorite(UserRecipeAbstract):

    class Meta(UserRecipeAbstract.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_favorite'
        )]
        default_related_name = 'favorites'


class Cart(UserRecipeAbstract):

    class Meta(UserRecipeAbstract.Meta):
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_carts'
        )]
        default_related_name = 'carts'