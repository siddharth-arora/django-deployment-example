from django.db import models
#import User object
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    #declare a foreign key object of the User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #additional features
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(blank=True,upload_to='profile_pics')

    #__str__()
    def __str__(self):
        return self.user.username
