from django.contrib import admin
from django.contrib.admin import display
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'in_favorites')
    readonly_fields = ('in_favorites',)
    list_filter = ('author', 'name', 'tags',)
    inlines = (RecipeIngredientInline,)

    @display(description='Количество в избранных')
    def in_favorites(self, obj):
        return obj.in_favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')