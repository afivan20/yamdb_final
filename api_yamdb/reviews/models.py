from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER_ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    username = models.SlugField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=150,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        'Эл. почта',
        help_text='Эл. почта пользователя',
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        help_text='Имя пользователя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        help_text='Фамилия пользователя',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        help_text='Биография пользователя',
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        help_text='Код подтверждения пользователя',
        max_length=200,
    )
    role = models.CharField(
        'Роль',
        help_text='Роль пользователя',
        max_length=150,
        blank=False,
        choices=USER_ROLES,
        default='user',
    )

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True

    @property
    def is_moderator(self):
        if self.role == 'moderator' or self.is_superuser:
            return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'username',
        )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        'Название',
        help_text='Название категории',
        max_length=200
    )
    slug = models.SlugField(
        'Идентификатор',
        help_text='Идентификатор категории (slug, уникальное)',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = (
            'pk',
        )

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(
        'Название',
        help_text='Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        'Идентификатор',
        help_text='Идентификатор жанра (slug, уникальное)',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = (
            'pk',
        )

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(
        'Название',
        help_text='Название произведения',
        max_length=200
    )
    year = models.IntegerField(
        'Год произведения',
        help_text='Год произведения (от 0 до текущего года)',
    )
    description = models.TextField(
        'Описание',
        help_text='Описание произведения',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория произведения',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        'Жанр',
        help_text='Жанр произведения',
        through='GenreTitle'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = (
            'pk',
        )

    def __str__(self):
        return self.name[:15]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title.name} {self.genre.name}'


class Review(models.Model):
    text = models.TextField(
        'Текст',
        help_text='Текст обзора',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор обзора',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(
        'Оценка',
        help_text='Оценка обзора',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата',
        help_text='Дата обзора',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        help_text='Обозреваемое произведение',
        related_name='reviews',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_title_author')
        ]
        ordering = (
            'pk',
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(
        'Комментарий',
        help_text='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        help_text='Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Ревью',
        help_text='Ревью в котором размещен комментарий',
        related_name='comments',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = (
            'pk',
        )

    def __str__(self):
        return self.text[:15]
