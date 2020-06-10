from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('notices/', views.notices, name="notices"),
    path('notices/add_notice', views.add_notice, name="add_notice"),
    path('notices/<id>', views.notice_detail, name="notice_detail"),
    path('notices/delete/<id>', views.delete_notice, name="delete"),
    path('profile/', include('users.urls'))
]