from django.urls import path

from book import views

urlpatterns=[
    path('book/',views.index,name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
]