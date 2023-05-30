from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    type=models.IntegerField(default=-1)

    def __str__(self):
        return '{}-{}'.format(self.user,self.type)

