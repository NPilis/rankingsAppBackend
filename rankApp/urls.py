from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls', namespace='user')),
    path('api/rankings/', include('ranking.urls', namespace='rankings')),
    path('api/auth/', include('authentication.urls', namespace='authentication')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)