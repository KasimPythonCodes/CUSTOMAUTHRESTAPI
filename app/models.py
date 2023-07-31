from django.db import models

# Create your models here.
class UserRegistration(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=150)
    
    def __str__(self):
        return self.first_name  +  '    '  + self.last_name
    
