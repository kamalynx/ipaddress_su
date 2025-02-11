from django.db import models
from django.urls import reverse_lazy
from uuid6 import uuid7


def article_directory_path(instance, filename):
    return f'uploads/articles/{instance.slug}/{filename}'


class Article(models.Model):
    id = models.UUIDField(default=uuid7, editable=False, primary_key=True)
    title = models.CharField(max_length=255, verbose_name="заголовок")
    description = models.CharField(
        max_length=1024, verbose_name="описание", blank=True
    )
    content = models.TextField(verbose_name="содержимое")
    slug = models.SlugField(max_length=255, verbose_name="URI")
    image = models.ImageField(
        upload_to=article_directory_path,
        max_length=255,
        blank=True,
        verbose_name='изображение',
    )
    published = models.BooleanField(
        default=False, verbose_name='опубликовано?'
    )
    created_at = models.DateTimeField(
        verbose_name="дата создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="дата обновления", auto_now=True
    )

    class Meta:
        ordering = ["created_at", "updated_at", "title"]
        verbose_name = "статья"
        verbose_name_plural = "статьи"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("articles:article", kwargs={"slug": self.slug})
