from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название места',
        help_text='Максимум 100 символов',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        ),
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:15]


class Post(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/images',
        blank=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.title[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время публикации',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text[:15]