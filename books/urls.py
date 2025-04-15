from django.urls import path
from . import views

urlpatterns = [
	path('book/detail/<str:pk>/', views.book_detail, name='book_detail')
]
