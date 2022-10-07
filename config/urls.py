from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # Local 
    path('', include('store.urls', namespace='store')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
