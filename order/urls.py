from django.urls import path
from order import views

urlpatterns= [
    path('checkout/', views.checkout),
    path('orders/',views.OrdersList.as_view()),
    path('order/pay/',views.payOrder),
    path('order/check/paystatus/', views.checkTransactionStatus)
]