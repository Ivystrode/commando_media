from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('notices/', views.notices, name="notices"),
    path('profile/', include('users.urls'))
]