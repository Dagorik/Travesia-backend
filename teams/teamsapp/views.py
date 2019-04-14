from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from teams.teamsapp.serializer import *
from teams.teamsapp.models import Teams, Race, Checkpoint, Track, Leaderboard
from teams.teamsapp.permissions import IsLeader
from django.db.models import Max, Min


class RetrieveTeams(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        teams = Teams.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class GetTeam(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        team = get_object_or_404(Teams, id=id)
        serializer = TeamMembersSerializer(team)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateTeam(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateTeamSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            team = serializer.save()
            request.user.is_leader = True
            request.user.save()
            return Response({"id": team.id, "code": team.members_code}, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class JoinTeam(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = JoinTeamSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            team = serializer.save()
            return Response({"message": "Member added successfuly"}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LeaveTeam(APIView):

    permission_classes = (IsAuthenticated, IsLeader)

    def post(self, request):
        serializer = LeaveSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Member Removed"}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ListCheckpoints(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        checks = Checkpoint.objects.all()
        serializer = CheckpointSerializer(checks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class GetCheckPoint(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        checks = get_object_or_404(Checkpoint, id=id)
        serializer = CheckpointSerializer(checks)
        return Response(serializer.data, status.HTTP_200_OK)


class AddTrack(APIView):

    permission_classes = (IsAuthenticated, IsLeader)

    def post(self, request):
        serializer = AddTrackSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            get_object_or_404(
                Checkpoint, id=serializer.validated_data['checkpoint'])
            data = serializer.save()
            return Response(data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_200_OK)


class CheckPosition(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        team = Teams.objects.filter(
            Q(leader=request.user) | Q(members=request.user)).first()
        tracks = Track.objects.filter(team=team).order_by('checkpoint').last()

        if(tracks):
            race_hour = tracks.checkpoint.carrera.all().first().start_hour
            position = Track.objects.filter(total_time__lt=tracks.total_time,
                                            checkpoint__num_checkpoint=tracks.checkpoint.num_checkpoint).count()
            laps_time = str(tracks.total_time-race_hour).split(' ')[2]
            hours, minutes, seconds = laps_time.split(':')
            print(hours,minutes,seconds)

            data = {
                "last_time": laps_time,
                "position": position+1,
                "num_checkpoint": tracks.checkpoint.num_checkpoint
            }
            status = 200
        else:
            data = {}
            status = 404
        return Response(data, status)


class LeaderBoardList(APIView):

    def get(self, request):
        leaderboard = Leaderboard.objects.all()
        serializers = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializers.data, status.HTTP_200_OK)
