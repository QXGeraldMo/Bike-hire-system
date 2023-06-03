import customers.views
from django.urls import path
from . import views

urlpatterns = [
    path('manager/login', views.MloginPage, name="managerlogin"),
    #path('manager/showpage', views.showpage, name='showpage'),
    path('manager/makequery', views.MakeQuery, name='makequery'),
    path('manager/makequery?page=<int:page>', views.MakeQuery),
    path("manager/visualization/view_1", views.view_1, name="view_1"),
    path("manager/visualization/view_2", views.view_2, name="view_2"),
    path("manager/visualization/view_3", views.view_3, name="view_3"),
    path("manager/visualization/view_4", views.view_4, name="view_4"),
    path("manager/visualization/view_5", views.view_5, name="view_5"),
    path("manager/logout", views.managerlogout, name="managerlogout")
]