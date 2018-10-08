from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name","last_name","email","password")
    
    def create(self,validated_data):
       return User.objects.create_user(**validated_data)



