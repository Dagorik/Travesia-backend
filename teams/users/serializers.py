from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from teams.users.MailService import SendMail

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.users.models import User,Codes
from teams.teamsapp.serializer import TeamSerializer
from teams.teamsapp.models import Teams

import datetime


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER




class UserSerializer(serializers.ModelSerializer):

    team =  serializers.SerializerMethodField()
    

    class Meta:
        model =  User
        exclude = ("username","password")

    def get_team(self,user):
        try:
            team = Teams.objects.filter(Q(leader=user) | Q(members=user))
            return TeamSerializer(team[0]).data
        except:
            return {}

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("username",)
    
    def create(self,validated_data):
       user = User.objects.create_user(username=validated_data['email'],is_active=False,**validated_data)
       code = Codes.objects.create(user=user,type_code="AC")
       mail = SendMail(email=user.email,code=code.code)
       mail.new_account_activate()
       return user


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
        return (token,self.user)

class ActivateSerializer(serializers.Serializer):

    email =  serializers.EmailField()
    code = serializers.CharField(max_length=10)

    def validate(self,data):
        exists_code = get_object_or_404(Codes,user__email=data['email'],code=data['code'])
        if exists_code:
            if not  exists_code.is_used and exists_code.ends_at > timezone.now() :
                return data
            else:
                raise serializers.ValidationError("Code expired or is used ")    
        else:
            raise serializers.ValidationError("Code does not exist or is invalid")


    def create(self,validated_data):
        data =  validated_data
        exists_code = get_object_or_404(Codes,user__email=data['email'],code=data['code'])
        exists_code.user.is_active = True
        exists_code.is_used = True
        exists_code.user.save()
        exists_code.save()
        payload = jwt_payload_handler(exists_code.user)
        token = jwt_encode_handler(payload)
        return token
    






        
