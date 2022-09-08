from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from store_django.settings import MPESA_API_BASE_URL
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer
import requests
import json

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    print(request.data)
    payNow = request.data.pop('payNow')
    serializer = OrderSerializer(data = request.data)
    
    if serializer.is_valid():
        amount_due = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'] )
        try:
            if payNow:
                response= send_stk_request(str(request.data.get('phone')), str(int(amount_due)))
                jsonResponse = json.loads(response.text)
                print("Response status code is "+ str(response.status_code))
                errorMessage = jsonResponse.get('errorMessage')
                if response.status_code > 299:
                    if errorMessage is not None:
                        print("Error message-> " + errorMessage)
                        return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"Error": "Undefined"},status=status.HTTP_502_BAD_GATEWAY)
            
                #at this point, we cannot confirm that the items have actually been paid for:
                checkoutRequestID = jsonResponse.get('Response').get('CheckoutRequestID')
                print(checkoutRequestID)
                checkoutRequestID_dict = {"CheckoutRequestID": checkoutRequestID}
                try:
                    serializer.save(user = request.user, amount_due = amount_due, checkoutRequestId = checkoutRequestID, paid = False)
                except Exception as e:
                    print(e)
                return Response(checkoutRequestID_dict, status = status.HTTP_201_CREATED)
            else:
                print("This customer will pay later....")
                try:
                    serializer.save(user = request.user, amount_due = amount_due, paid = False)
                except Exception as e:
                    print(e)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    print(serializer.errors)
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


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def payOrder(request):
    print(request.data)
    serializer = OrderSerializer(Order.objects.get(id = request.data.get('id')), data={'id': request.data.get('id')})
    try:
        amount_due = str(int(float(request.data.get('amount_due'))))
        phone = str(request.data.get('phone'))
        
        response= send_stk_request(phone, amount_due)
        jsonResponse = json.loads(response.text)
        print("Response status code is "+ str(response.status_code))
        errorMessage = jsonResponse.get('errorMessage')
        if response.status_code > 299:
            if errorMessage is not None:
                print("Error message-> " + errorMessage)
                return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Error": "Undefined"},status=status.HTTP_502_BAD_GATEWAY)
    
        #at this point, we cannot confirm that the items have actually been paid for:
        checkoutRequestID = jsonResponse.get('Response').get('CheckoutRequestID')
        print(checkoutRequestID)
        checkoutRequestID_dict = {"CheckoutRequestID": checkoutRequestID}
        try:
            if serializer.is_valid():
                serializer.save(checkoutRequestId = checkoutRequestID)
        except Exception as e:
            print(e)
        return Response(checkoutRequestID_dict, status = status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

def send_stk_request(phoneNumber, amount):
    """ 
        Important!!
        Remember to add a name and password with HTTPBasicAuth
    """
    data = {
            "phone": phoneNumber,
            "amount": amount,
            "shortcode": "174379",
            "AccountReference": "Boots Kenya",
            "ApplicationId": "0001"
        }
    headers = {"Content-Type": "application/json"}
    api_url = f"https://{MPESA_API_BASE_URL}/stk/"
    print("Sending stk push request........");
    response = requests.post(api_url,json=data, headers=headers)
    return response


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkTransactionStatus(request):
    print(request.data)
    return Response({}, status=status.HTTP_200_OK)