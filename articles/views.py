from django.shortcuts import render
from django.views import generic

from articles import models


class ArticleDetail(generic.DetailView):
    model = models.Article
    queryset = models.Article.objects.filter(published=True)
    template_name = "articles/single.html"
    context_object_name = "article"


class ArticleList(generic.ListView):
    model = models.Article
    queryset = models.Article.objects.filter(published=True)
    template_name = "articles/index.html"
    context_object_name = "articles"
