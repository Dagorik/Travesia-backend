from django.shortcuts import render
from teams.users import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SignupView(APIView):

    def post(self,request):
        serializer =  serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user =  serializer.save()
            data = {"message":"User created","id":user.id}
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
   

   def post(self,request):
        serializer =  serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            token =  serializer.save()
            data = {"token":token}
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



