from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('show_all_vehicles/', views.show_all_vehicles, name="show_all_vehicles"),
    path('register/', views.registerPage, name='register'),
    path('image/code/', views.image_code),
    path('hire_vehicle/', views.hire_vehicle, name='hire_vehicle'),
    path('duration_price/', views.duration_price, name='duration_price'),
    path('payment/', views.payment, name='payment'),
    path('report/', views.report, name='report'),
    path('', views.index, name="index"),

]
