
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from scraping.sitemap import PostsSitemap, StaticViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostsSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scraping.urls')),
    path('api/', include('rest_framework.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('robots.txt', include('robots.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]

urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
