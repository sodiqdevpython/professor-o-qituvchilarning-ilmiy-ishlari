from django.urls import path
from .views import *

urlpatterns = [
	path('', UserDashboard.as_view(), name='user_dashoard'),
	path('user-documents/', UserDocumentsView.as_view(), name='user_docs'),
	path('user-books/', UserBooksView.as_view(), name='user_books'),
	path('docs-create/', DocumentCreateView.as_view(), name='create_docs'),
	path('books-create/', BookCreateView.as_view(), name='create_books')
]
