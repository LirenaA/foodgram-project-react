from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser, null=True,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписываться на самого себя')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_object'
        )]

    def __str__(self):
        return f'{self.user} <-> {self.author}'
