from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from teams.teamsapp.serializer import CreateTeamSerializer,JoinTeamSerializer
# Create your views here.


class CreateTeam(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        serializer =  CreateTeamSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            team = serializer.save()
            return Response({"id":team.id,"code":team.members_code},status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class JoinTeam(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        serializer = JoinTeamSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            team = serializer.save()
            return Response({"message":"Member added successfuly"},status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)



