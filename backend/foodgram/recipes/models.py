from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        blank=True,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
    )
    cooking_time = models.PositiveIntegerField()
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/images/'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    in_carts = models.ManyToManyField(
        User,
        through='Cart',
        related_name='recipes_in_cart'
    )
    in_favorites = models.ManyToManyField(
        User,
        through='Favorite',
        related_name='recipes_in_favorite'
    )


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredient_amount'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_amount'
    )
    amount = models.PositiveIntegerField()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранные'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_favorite'
        )]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='carts',
    )

    class Meta:
        verbose_name = 'Корзина'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_carts'
        )]
