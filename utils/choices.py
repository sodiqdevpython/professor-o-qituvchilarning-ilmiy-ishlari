from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class UserTypeChoices(TextChoices):
	TEACHER = "OQ", _("O'qituvchi")
	MUDIR = "KM", _("Kafedra mudiri")
	DEKAN = "DK", _("Dekan")
	PROREKTOR = "PR", _("Prorektor")
	REKTOR = "RE", _("Rektor")