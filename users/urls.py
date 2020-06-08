from django.urls import path, include
from . import views

urlpatterns = [
    path('<username>/', views.profile, name="profile"),
]

# Goal - to make users' profile pages viewable to all users, editable only by the user who owns the page.