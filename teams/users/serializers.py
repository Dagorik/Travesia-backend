from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.users.models import User
from teams.teamsapp.serializer import TeamSerializer
from teams.teamsapp.models import Teams




jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER




class UserSerializer(serializers.ModelSerializer):

    team =  serializers.SerializerMethodField()
    

    class Meta:
        model =  User
        exclude = ("username",)

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

