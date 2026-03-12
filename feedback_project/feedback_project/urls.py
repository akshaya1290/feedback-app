from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feedback.urls')),
]

# Serve frontend files and static files
if settings.DEBUG:
    # Serve static files from frontend directory
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Also serve any .css, .js, .html files directly from frontend root
    urlpatterns += [
        re_path(r'^(?P<path>.*\.css)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
        re_path(r'^(?P<path>.*\.js)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)