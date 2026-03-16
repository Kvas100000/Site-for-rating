from django.urls import reverse
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name

class Content(models.Model):
    class Type(models.TextChoices):
        MOVIE = 'MOVIE', 'Фильм'
        GAME = 'GAME', 'Игра'
        SERIES = 'SERIES', 'Сериал'
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True,verbose_name= "Описание")
    release_year = models.PositiveIntegerField(verbose_name="Год выпуска")
    category = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.MOVIE,
        verbose_name="Категория"
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='contents',
        verbose_name="Жанры"
    )
    poster = models.ImageField(blank=True,upload_to='posters/')
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL Slug")


    def __str__(self):
        return f"[{self.category}] {self.title}"

    def get_average_score(self):
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else 0.0

    def get_absolute_url(self):
        return reverse('main:content_detail', kwargs={'slug': self.slug})

class Movie(Content):
    director = models.CharField(max_length=100,verbose_name= 'Режиссер')
    actors = models.TextField(blank=True, verbose_name="Актеры")
    duration = models.PositiveIntegerField(verbose_name="Длительность")

class Game(Content):
    developer = models.CharField(max_length=100,verbose_name=" Разработчики")
    publisher = models.CharField(max_length=100,verbose_name=" Издатель")
    system_requirements = models.TextField(blank = True,verbose_name=" Системные требования")

class Series(Content):
    class Status(models.TextChoices):
        ONGOING = 'ONGOING', 'Выходит'
        ENDED = 'ENDED', 'Завершен'
        CANCELED = 'CANCELED', 'Закрыт'
        PAUSED = 'PAUSED', 'Приостановлен'
        ANNOUNCED = 'ANNOUNCED', 'Анонс'
    seasons_count = models.PositiveIntegerField(verbose_name="Количество сезонов")
    status = models.CharField(max_length=15,choices=Status.choices,default=Status.ONGOING,verbose_name="Статус производства")
    director = models.CharField(max_length=100, verbose_name='Режиссер')
    actors = models.TextField(blank=True ,verbose_name="Актеры")

    def get_status_color(self):
        if self.status == self.Status.ONGOING:
            return 'success'
        elif self.status == self.Status.ENDED:
            return 'secondary'
        elif self.status == self.Status.CANCELED:
            return 'danger'
        elif self.status == self.Status.ANNOUNCED:
            return 'info'
        return 'warning'


class Screenshot(models.Model):
    content = models.ForeignKey(Content, related_name='scrins', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scrins/')

    def __str__(self):
        return f"Скриншот для {self.content.title}"

class Rating(models.Model):
    class Status(models.TextChoices):
        WATCHED = 'WATCHED', 'Просмотрено'
        PLANNING = 'PLANNING', 'В планах'
        FAVORITE = 'FAVORITE', 'Любимое'

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_ratings')
    score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],verbose_name="Оценка",null=True, blank=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.WATCHED,verbose_name="Статус")
    review = models.TextField(blank=True, null=True,verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')

