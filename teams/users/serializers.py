from rest_framework import serializers
from teams.users.models import User

from rest_framework_jwt.settings import api_settings

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name","last_name","email","password","birth_date","gender","phone")
    
    def create(self,validated_data):
       return User.objects.create_user(username=validated_data['email'],**validated_data)


class LoginSerializer(serializers.Serializer):

    email =  serializers.EmailField()
    password =  serializers.CharField(max_length=150)


    def validate(self,data):
        
        user = get_user_model().objects.get(email__iexact=data['email'])
        if check_password(data['password'], user.password):
            self.user = user
            return {"id":user.id,"email":user.email}
        else:
            raise serializers.ValidationError("email or password are incorrect")

    def create(self,validated_data):
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        return token

