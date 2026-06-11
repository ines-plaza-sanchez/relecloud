from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('relecloud.urls')),
    path('admin/', admin.site.urls),
    # allauth: login, logout, signup, password reset, etc.
    path('accounts/', include('allauth.urls')),
]

# PT2: servir imágenes subidas en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
