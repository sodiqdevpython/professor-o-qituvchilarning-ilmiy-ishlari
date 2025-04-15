from django.urls import path
from .views import DashboardView, users_list, add_user, user_detail, user_update, scientific_works, books, LoginView, performance_table, performance_download
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path('', DashboardView.as_view(), name='admin_dashboard'),
	path('users/', users_list, name='users_list'),
	path('add-user/', add_user, name='user_add'),
	path('user-detail/<str:pk>/', user_detail, name='user_detail'),
	path('user-update/<uuid:pk>/', user_update, name='user_update'),
	path('docs/', scientific_works, name='docs'),
	path('books/', books, name='books'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('login/', LoginView.as_view(), name='login'),
	path('statistic/', performance_table, name='performance_table'),
	path('statistic/download/<str:format>/', performance_download, name='performance_download'),
]
