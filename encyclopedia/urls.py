from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/', views.search_entry, name='search_entry'),
    path('wiki/<str:entry>', views.entry, name='wiki'),
]
