from django.urls import path

from articles import views


app_name = "articles"

urlpatterns = [
    path("", views.ArticleList.as_view(), name="index"),
    path("<slug:slug>/", views.ArticleDetail.as_view(), name="article"),
]
