from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ideas, name="ideas"),
    path('add_idea', views.add_idea, name="add_idea"),
    path('<id>', views.idea_detail, name="idea_detail"),
    path('<id>/delete', views.delete_idea, name="delete_idea"),
    path('<id>/edit_idea', views.edit_idea, name="edit_idea"), # why does this load the add idea template (but still work?)
]