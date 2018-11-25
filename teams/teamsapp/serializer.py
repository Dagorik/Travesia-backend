from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models  import Q
from teams.teamsapp.models import Teams
from teams.users.models import User
from teams.users import serializers  as ser

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('first_name',"last_name","email",
                    "birth_date","gender","phone","is_leader",
                    "profile_pic")


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Teams
        fields = ('id','name','logo','mantra','created_at','is_active','leader','members_code')


class TeamMembersSerializer(serializers.ModelSerializer):
    members =  UserSimpleSerializer(many=True)

    class Meta:
        model =  Teams
        fields = ('id','name','logo','mantra','created_at','is_active','leader','members')


class CreateTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teams
        fields = ("name",)

    
    def create(self,validated_data):
        return Teams.objects.create(
            leader=self.context['request'].user,
            name=validated_data["name"]
        )


class JoinTeamSerializer(serializers.ModelSerializer):


    class Meta:
        model = Teams
        fields = ('members_code',)

    def validate(self,data):
        user = self.context['request'].user
        if Teams.objects.filter(members_code=data.get('members_code')).exists():
            if not Teams.objects.filter(Q(leader=user) | Q(members=user)):
                return data
            else:
                raise serializers.ValidationError("Member is in another team")
        else:
            raise serializers.ValidationError("Members Code does not exist")
    
    def create(self,validated_data):
        code =  validated_data['members_code']
        team = Teams.objects.get(members_code=code)
        user = self.context['request'].user
        team.members.add(user)
        return team
    

class LeaveSerializer(serializers.Serializer):

    id_team =  serializers.CharField(max_length=150)

    
