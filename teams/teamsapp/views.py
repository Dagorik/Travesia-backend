from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from teams.teamsapp.serializer import CreateTeamSerializer
# Create your views here.


class CreateTeam(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        serializer =  CreateTeamSerializer(data=request.body)
        if serializer.is_valid():
            team = serializer.save()
            return Response({"id":team.id,"code":team.members_code},status.HTTP_201_CREATED)
        else:
            return Response({"message":"Error to create team",status.HTTP_400_BAD_REQUEST})