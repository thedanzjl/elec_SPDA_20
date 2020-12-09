from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    number = models.IntegerField(primary_key=True, unique=True)
    users = models.ManyToManyField(User)
    sign_date = models.DateField(null=True, blank=True)
    sign_status = models.BooleanField(default=False)
    path = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.number)
