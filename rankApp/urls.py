from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls', namespace='user')),
    path('api/rankings/', include('ranking.urls', namespace='rankings')),
    path('api/auth/', include('authentication.urls', namespace='authentication')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
]
