from django.urls import path
from operators import views
urlpatterns = [
    # path('operators/', views.operators),
    # path('operators/move/', views.operators_move),
    # path('track/', views.operators_track),
    # path('operators/charge/', views.operators_charge),
    # path('operators/repair/', views.operators_repair),

    path('', views.operators, name="index"),
    path('operators/', views.operators, name="operators"),
    path('track/', views.operators_track, name="track"),
    path('charge/', views.operators_charge, name="charge"),
    path('repair/', views.operators_repair, name="repair"),
    path('move/', views.operators_move, name="move"),
    path('loginoperator/', views.loginOperator, name="loginOperator"),
    path('logoutoperator/', views.logoutOperator, name="logoutOperator"),
]