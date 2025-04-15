from django.db import models
from utils.models import BaseModel
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

class DocumentTypeSubtitles(BaseModel):
	name = models.CharField(max_length=128)

	def __str__(self):
		return self.name

class DocumentType(BaseModel):
	name = models.CharField(max_length=128)
	subtitle = models.ForeignKey(DocumentTypeSubtitles, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name

class Document(BaseModel):
	name = models.CharField(max_length=512)
	type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
	author = models.ForeignKey('users.User', on_delete=models.CASCADE)
	file = models.FileField(upload_to='documents/', validators=[
		FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'xlsm'], message=_("Bunday fayl formati qo'llab quvvatlanmaydi"))
	])
	url = models.URLField(null=True, blank=True)
	image = models.ImageField(upload_to='document-images/', validators=[
		FileExtensionValidator(
			allowed_extensions=['png', 'jpg', 'jpeg', 'webp'], message=_("Bunday fayl formati qo'llab quvvatlanmaydi")
		)
	])
	more_info = models.TextField(null=True, blank=True)
	is_confirmed = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name
	
class Requirements(BaseModel):
	user = models.ForeignKey('users.User', on_delete=models.CASCADE)
	document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
	numbers = models.PositiveIntegerField(default=0)
	in_use = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.user)