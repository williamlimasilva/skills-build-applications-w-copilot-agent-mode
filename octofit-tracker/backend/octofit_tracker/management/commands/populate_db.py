from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Team Marvel')
        dc = Team.objects.create(name='Team DC')

        # Create Users
        users = [
            User(email='ironman@marvel.com', username='ironman', team=marvel),
            User(email='captain@marvel.com', username='captain', team=marvel),
            User(email='batman@dc.com', username='batman', team=dc),
            User(email='superman@dc.com', username='superman', team=dc),
        ]
        for user in users:
            user.set_password('password123')
            user.save()

        # Create Activities
        activities = [
            Activity(user=users[0], type='run', duration=30, calories=300),
            Activity(user=users[1], type='cycle', duration=45, calories=400),
            Activity(user=users[2], type='swim', duration=60, calories=500),
            Activity(user=users[3], type='walk', duration=20, calories=100),
        ]
        Activity.objects.bulk_create(activities)

        # Create Workouts
        workouts = [
            Workout(name='Morning Cardio', description='Cardio for all'),
            Workout(name='Strength Training', description='Strength for all'),
        ]
        Workout.objects.bulk_create(workouts)

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=700)
        Leaderboard.objects.create(team=dc, points=600)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))

# Models for reference (should be in octofit_tracker/models.py):
# class Team(models.Model):
#     name = models.CharField(max_length=100)
#
# class Activity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=50)
#     duration = models.IntegerField()
#     calories = models.IntegerField()
#
# class Workout(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
# class Leaderboard(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     points = models.IntegerField()
