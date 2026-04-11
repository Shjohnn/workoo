from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog

from jobs.views import home_view
from ishtop.views import set_language as set_language_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Custom set_language: fixes redirect uz <-> /ru/ when prefix_default_language=False
    path('i18n/setlang/', set_language_view, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('', home_view, name='home'),
    path('ishlar/', include('jobs.urls')),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('baholar/', include('ratings.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript_catalog'),
    prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
