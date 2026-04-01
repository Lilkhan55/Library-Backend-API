"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from library.views import page_not_found
from django.conf.urls.static import static
from . import settings
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

from debug_toolbar.toolbar import debug_toolbar_urls

from library.sitemaps import LibSitemap, GenreSitemap, TagSitemap

sitemaps = {
    'libs': LibSitemap,
    'genre': GenreSitemap,
    'tagbook': TagSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls', namespace='library')),
    path('users/', include('users.urls', namespace='users')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные книги"
