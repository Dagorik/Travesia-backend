from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models import Q
from teams.teamsapp.models import Teams, Race, Checkpoint, Track, Leaderboard
from teams.users.models import User
from teams.users import serializers as ser
import datetime


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', "last_name", "email",
                  "birth_date", "gender", "phone", "is_leader",
                  "profile_pic")


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo', 'mantra', 'created_at',
                  'is_active', 'leader', 'members_code')


class TeamMembersSerializer(serializers.ModelSerializer):
    members = UserSimpleSerializer(many=True)
    leader = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Teams
        fields = ('id', 'name', 'logo', 'mantra', 'created_at',
                  'is_active', 'leader', 'members')


class CreateTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teams
        fields = ("name",)

    def create(self, validated_data):
        return Teams.objects.create(
            leader=self.context['request'].user,
            name=validated_data["name"]
        )


class JoinTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teams
        fields = ('members_code',)

    def validate(self, data):
        user = self.context['request'].user
        if Teams.objects.filter(members_code=data.get('members_code')).exists():
            if not Teams.objects.filter(Q(leader=user) | Q(members=user)):
                return data
            else:
                raise serializers.ValidationError("Member is in another team")
        else:
            raise serializers.ValidationError("Members Code does not exist")

    def create(self, validated_data):
        code = validated_data['members_code']
        team = Teams.objects.get(members_code=code)
        user = self.context['request'].user
        team.members.add(user)
        return team


class LeaveSerializer(serializers.Serializer):
    id_user = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = self.context['request'].user
        team = Teams.objects.get(leader=user)
        team.members.remove(validated_data['id_user'])
        return team


class CheckpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkpoint
        exclude = ('qrcode',)


class LeaderboardSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Leaderboard
        exclude = ('id',)


class AddTrackSerializer(serializers.Serializer):

    checkpoint = serializers.UUIDField()
    check_time = serializers.DateTimeField()
    members = serializers.IntegerField()

    def validate(self, data):
        user = self.context['request'].user
        team = user.equipo.all().first()
        print(team.members)
        if Track.objects.filter(team=team.id, checkpoint=data['checkpoint']).exists():
            raise serializers.ValidationError("Team did this checkpoint")
        elif Teams.objects.get(id=team.id).members.count() < data['members']:
            raise serializers.ValidationError(
                "Can not exceed the number of members")
        else:
            return data

    def calculate_penalization(self, time, penalization):
        return time + datetime.timedelta(minutes=penalization)

    def create_or_update_leaderboard(self, track, total_time, current):
        hours, minutes, seconds = current.split(':')
        if track.checkpoint.is_final:
            print(track.team.id)
            if Leaderboard.objects.filter(team=track.team).exists():
                lead = Leaderboard.objects.get(team=track.team)
                lead.time = total_time.strftime("%Y-%m-%d %H:%M:%S")
                lead.hours = lead.hours+int(hours)
                lead.minutes = lead.minutes+int(minutes)
                lead.seconds = lead.seconds+int(seconds)
                print(total_time, lead.time)
                lead.save()
            else:
                lead = Leaderboard.objects.create(
                    team=track.team, time=track.total_time, hours=int(hours),
                    minutes=int(minutes), seconds=int(seconds)
                )

    def create(self, validated_data):
        user = self.context['request'].user
        team = Teams.objects.get(leader=user)
        checkpoint = Checkpoint.objects.get(
            id=validated_data['checkpoint'])
        penalization = (team.members.count() - validated_data['members'])*20
        total_time = self.calculate_penalization(
            validated_data['check_time'], penalization) if penalization > 0 else validated_data['check_time']
        race = checkpoint.carrera.all().first()
        if race:
            current = str(total_time - race.start_hour).split(' ')[2]
            hours, minutes, seconds = current.split(':')
            print(hours, minutes, seconds)
            track = Track.objects.create(team=team,
                                         checkpoint=checkpoint,
                                         check_time=validated_data['check_time'],
                                         penalization=penalization,
                                         total_time=total_time,
                                         hours=int(hours),
                                         minutes=int(minutes),
                                         seconds=int(seconds)
                                         )
            self.create_or_update_leaderboard(track, total_time, current)
            return {"current_time": str(current), "num_checkpoint": checkpoint.num_checkpoint}
        else:
            raise serializers.ValidationError("Not set race")
