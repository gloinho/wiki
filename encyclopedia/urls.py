from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/', views.search_entry, name='search_entry'),
    path('wiki/<str:entry>', views.entry, name='wiki'),
    path('new_page', views.new_page, name='new_page'),
    path('edit_page/<str:page>', views.edit_page, name='edit_page'),
]
