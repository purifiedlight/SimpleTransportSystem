from django.urls import path
from TransportApp import views

urlpatterns = [
    path('transportorder/', views.transportorderApi, name='transportorder-list'), 
    path('transportorder/<int:id>/', views.transportorderApi, name='transportorder-detail'),
]