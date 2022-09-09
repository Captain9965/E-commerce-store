from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from store_django.settings import MPESA_API_BASE_URL,MPESA_SHORT_CODE
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
    checkoutRequestID_dict = {}
    try:
        order = Order.objects.get(id = request.data.get('id'))
        """
         the customer may have paid but not confirmed....
         take note that the source of truth is the database..
        """

        if(order.checkoutRequestId):
            print(order.checkoutRequestId)
            response = send_status_request(order.checkoutRequestId)
            jsonResponse = json.loads(response.text)
            print("Response status code is "+ str(response.status_code))
            response_payload = jsonResponse.get('Response')
            print(response_payload)
            if not response.status_code > 299:
            #in this case, the transaction exists on the backend, we just need to check whether it succeeded or failed
                if response_payload.get('Service status') == "success":
                    print("Client has paid...")
                    order.paid = True
                    order.result_description = response_payload.get('ResultDesc')
                    if response_payload.get('MpesaReceiptNumber'):
                        order.transaction_id = response_payload.get('MpesaReceiptNumber')
                    order.save()
                    return Response({"Info": "no confirmation needed"}, status=status.HTTP_200_OK)

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
            order.checkoutRequestId = checkoutRequestID
            order.save()
        except Exception as e:
            print(e)
        return Response(checkoutRequestID_dict, status = status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkTransactionStatus(request):
    if "checkoutRequestID" not in request.data:
        return Response({"Error": "CheckoutRequestID missing from payload"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        response = send_status_request(request.data.get('checkoutRequestID'))
        jsonResponse = json.loads(response.text)
        print("Response status code is "+ str(response.status_code))
        errorMessage = jsonResponse.get('errorMessage')
        if response.status_code > 299:
            if errorMessage is not None:
                print("Error message-> " + errorMessage)
                return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Error": "Undefined"},status=status.HTTP_502_BAD_GATEWAY)
            
        #At this point we are certaint that the customer has paid for the items:   
        response_payload = jsonResponse.get('Response')
        print(response_payload)
        #we can now reconcile the order:
        try:
            order = Order.objects.get(checkoutRequestId = response_payload.get('CheckoutRequestID'))
            if order is not None:
                order.result_description = response_payload.get('ResultDesc')
                order.paid = True if response_payload.get('Service status') == "success" else False
                if response_payload.get('MpesaReceiptNumber'):
                    order.transaction_id = response_payload.get('MpesaReceiptNumber')
                order.save()
                if response_payload.get('Service status') == "success":
                    print("Client has paid...")
                    return Response({}, status=status.HTTP_200_OK)
                print("Client has not paid...")
                return Response({"Error": "Not paid"}, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response({"Error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(e)
        return Response({"Error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)



def send_stk_request(phoneNumber, amount):
    """ 
        Important!!
        Remember to add a name and password with HTTPBasicAuth
    """
    data = {
            "phone": phoneNumber,
            "amount": "1",
            "shortcode": f"{MPESA_SHORT_CODE}",
            "AccountReference": "Boots Kenya",
            "ApplicationId": "0001"
        }
    headers = {"Content-Type": "application/json"}
    api_url = f"https://{MPESA_API_BASE_URL}/stk/"
    print("Sending stk push request........");
    response = requests.post(api_url,json=data, headers=headers)
    return response

def send_status_request(checkoutRequestID):
    data = {
            "shortcode": f"{MPESA_SHORT_CODE}",
            "ApplicationId": "0001",
            "CheckoutRequestID": checkoutRequestID
        }
    headers = {"Content-Type": "application/json"}
    api_url = f"https://{MPESA_API_BASE_URL}/stk/checkStatus"
    print("Sending status request........");
    response = requests.post(api_url,json=data, headers=headers)
    return response
