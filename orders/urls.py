from django.urls import path
from . import views
from uuid import UUID

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('cancel/<uuid:pk>/', views.cancel_order_view, name='cancel'),
]