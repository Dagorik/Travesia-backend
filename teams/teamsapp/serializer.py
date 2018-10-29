from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from teams.teamsapp.models import Teams



class CreateTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teams
        fields = ("name",)

    
    def create(self,validated_data):
       return Teams.objects.create(
            leader=CurrentUserDefault(),
            name=validated_data["name"]
        )
