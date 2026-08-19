from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),

    # Toutes les pages du magazine
    path('', include('magazine.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)