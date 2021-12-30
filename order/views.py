from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
#import also the mpesa api
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data = request.data)
    
    if serializer.is_valid():
        #initialize mpesa
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'] )
        try:
            #process payment
            print("This is the user on checkout: ")
            print(request.user)
            serializer.save(user = request.user,paid_amount = paid_amount)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    print("serializer error")
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
     authentication_classes = [authentication.TokenAuthentication]
     permission_classes = [permissions.IsAuthenticated]

     def get(self,request, format = None):
         print("This is the user on orders: ")
         print(request.user)
         orders = Order.objects.filter(user=request.user)
         serializer = MyOrderSerializer(orders, many=True)
         return Response(serializer.data)