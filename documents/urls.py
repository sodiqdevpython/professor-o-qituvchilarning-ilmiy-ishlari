from django.urls import path
from .views import DashboardView, document_detail

urlpatterns = [
	path('', DashboardView.as_view()),
	path('document-detail/<str:pk>/', document_detail, name='document_detail')
]
