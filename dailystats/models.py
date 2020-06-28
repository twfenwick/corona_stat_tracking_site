from django.db import models


class State(models.Model):
    state_name = models.CharField(max_length=50)
    state_code = models.CharField(max_length=2)


class County(models.Model):
    county_name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
