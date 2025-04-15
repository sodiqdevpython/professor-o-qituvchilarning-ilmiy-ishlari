from django.db import models
from utils.models import BaseModel
from utils import choices
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class Faculty(models.Model):
    name = models.CharField(max_length=256, unique=True)
    admin = models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='managed_faculty',null=True,blank=True)

    def __str__(self):
	    return self.name

class User(AbstractUser, BaseModel):
	tel_number = models.CharField(max_length=9, unique=True)
	type = models.CharField(max_length=2, choices=choices.UserTypeChoices.choices, null=True)
	faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
	profile_image = models.ImageField(upload_to='user/', validators=[
		FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'webp'])
	], null=True, blank=True)

	def __str__(self):
		return self.first_name