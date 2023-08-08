from django.db import models
from django.contrib.auth import get_user_model

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient', 
                                         through='RecipeIngredient')
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/images/'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()   