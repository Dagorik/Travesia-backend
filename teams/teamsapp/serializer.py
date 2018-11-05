from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models  import Q
from teams.teamsapp.models import Teams



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
