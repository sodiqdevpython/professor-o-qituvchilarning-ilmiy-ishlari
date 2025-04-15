from django.db import models
from utils.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class BookType(models.Model):
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return self.name

class Book(BaseModel):
	name = models.CharField(max_length=256)
	type = models.ForeignKey(BookType, on_delete=models.CASCADE)
	file = models.FileField(upload_to='documents/', validators=[
		FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'xlsm'], message=_("Bunday fayl formati qo'llab quvvatlanmaydi"))
	])
	image = models.ImageField(upload_to='books/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
	author = models.ForeignKey('users.User', on_delete=models.CASCADE)
	more_info = models.TextField(null=True, blank=True)
	is_confirmed = models.BooleanField(default=False)

	def __str__(self):
		return self.name