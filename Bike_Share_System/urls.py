from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customers.urls')),
    path('', include('operators.urls')),
    path('', include('manager.urls')),
    #path('', RedirectView.as_view(url='customers/', permanent=False)),

]
