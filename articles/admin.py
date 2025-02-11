from django.contrib import admin

from articles import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
