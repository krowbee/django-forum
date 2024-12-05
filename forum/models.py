from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(verbose_name="Ім'я", max_length=20, null=True)
    last_name = models.CharField(verbose_name="Фамілія", max_length=20, null=True)
    bio = models.TextField(verbose_name='Біографія', max_length=252, default='Опис відсутній')
    joined_date = models.DateField(verbose_name='Дата реєстрації', auto_now_add=True)
    user = models.OneToOneField(User, verbose_name='Користувач', related_name='profile', on_delete=models.CASCADE)
    filled = models.BooleanField(default=False, verbose_name='Заповнений')

    def __str__(self):
        return f'Профіль користувача {self.user.username}'

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"profile_id": self.id})


class Category(models.Model):
    name = models.CharField(verbose_name='Назва категорії', max_length=32)
    slug = models.SlugField(verbose_name='Slug', blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-topics", kwargs={"category_slug": self.slug})


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категорія', related_name='subcategory', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Назва підкатегорії', max_length=32)
    slug = models.SlugField(verbose_name='slug', blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("subcategory-topics", kwargs={"category_slug": self.category.slug, "subcategory_slug": self.slug})


class Topic(models.Model):
    title = models.CharField(verbose_name='Тема обговорення', max_length=72)
    content = models.TextField(verbose_name='Контент', max_length=1000)
    subcategory = models.ForeignKey(SubCategory, verbose_name='Під категорія', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("topic", kwargs={"category_slug": self.subcategory.category.slug,
                                        "subcategory_slug": self.subcategory.slug, "topic_id": self.id})

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField(verbose_name='Контент', max_length=1000)
    topic = models.ForeignKey(Topic, verbose_name='Обговорення', on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='post_author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def __str__(self):
        return f'{self.topic.title}, {self.author} '


class Comment(models.Model):
    content = models.TextField(verbose_name='Контент', max_length=1000)
    post = models.ForeignKey(Post, verbose_name='Пост', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', related_name='comment_author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')


class Like(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', verbose_name='Пост', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]
