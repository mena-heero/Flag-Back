from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views
from .wagtail_api import api_router
from affiliate.views import CreativeRedirectView


urlpatterns = [
    path("sitemap.xml", sitemap),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/v2/", api_router.urls),
    path("api/v1/auth/", include("authentication.urls", namespace="authentication")),
    path("api/v1/utility/", include("utility.urls", namespace="utility")),
    path("api/v1/home/", include("home.urls", namespace="home")),
    path("api/v1/company/", include("company.urls", namespace="company")),
    path("api/v1/affiliate/", include("affiliate.urls", namespace="affiliate")),
    path("visit/", CreativeRedirectView.as_view(), name="creative_redirect_view"),
    path('welcome/', include('landing.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
