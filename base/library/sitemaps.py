from django.contrib.sitemaps import Sitemap

from library.models import Book, Genre, TagPost

class LibSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Book.instock.all()
    
class GenreSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Genre.objects.all()
    
class TagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return TagPost.objects.all()
