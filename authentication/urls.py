from django.urls import path
from authentication import views
from knox import views as knox_views

app_name = 'auth'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]