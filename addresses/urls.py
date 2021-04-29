from django.conf.urls import url, include
from addresses import views
from django.urls import path

urlpatterns = [
    path('addresses/', views.address_list),
    path('addresses/<int:pk>/', views.address),
    # path('addresses/<String:name>/', views.addressName),
    # path('login/', views.login),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework'))
]

## addresses 로오면 address_list실행