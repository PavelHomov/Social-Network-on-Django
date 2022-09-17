from django.db import models
from django.contrib.auth import get_user_model

from .constants import POSTS_SYMBOLS

User = get_user_model()


class Group(models.Model):
    """Модель Group."""
    title = models.CharField(
        verbose_name="Название группы",
        max_length=200,
        help_text="Введите название группы",
    )
    slug = models.SlugField(
        verbose_name="Slug группы",
        unique=True,
        help_text="Введите адрес группы",
    )
    description = models.TextField(
        verbose_name="Описание группы",
        help_text="Введите описание",
    )

    def __str__(self) -> str:
        """Метод вывода названия группы."""
        return self.title


class Post(models.Model):
    """Модель Post."""
    text = models.TextField(
        verbose_name="Текст поста",
        help_text="Введите текст поста",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор",
        help_text="Укажите автора поста",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name="Группа",
        help_text="Укажите группу",
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        """Метод возвращает первые 15 символов поста."""
        return self.text[:POSTS_SYMBOLS]


class Comment(models.Model):
    """Модель Comment."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пост",
        help_text="Пост для комментария",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор",
        help_text="Автор комментария",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Введите текст комментария",
    )
    created = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
