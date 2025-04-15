from django.db import models
from uuid import uuid4
from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True, unique=True)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	updated = models.DateTimeField(auto_now=True, editable=False)
	is_deleted = models.BooleanField(default=False, editable=False)
	history = HistoricalRecords(inherit=True)

	class Meta:
		abstract = True