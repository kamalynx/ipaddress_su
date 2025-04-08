from django.contrib.sitemaps import Sitemap

from articles.models import Article


class ArticlesSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.created_at
