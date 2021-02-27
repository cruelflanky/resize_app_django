from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('load-image/', views.load_image, name="load-image"),
	path('load-image/change-size/<str:pk>/', views.change_size, name="change-size"),
]