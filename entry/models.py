from __future__ import unicode_literals


from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

from patients.models import Patient

def upload_location(instance, filename):
	return "images/%s" % (filename)

# Create your models here.
class Entry(models.Model):
	
	user_id = models.IntegerField(default=1)
	title = models.CharField(max_length=120, blank=True)
	meal_type = models.CharField(max_length=120, blank=True)
	content = models.TextField(blank=True)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	image = models.ImageField(upload_to = upload_location, 
		null=True, 
		blank=True, 
		height_field="height_field", 
		width_field="width_field")
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("entry:detail", kwargs={"id" : self.id})

	class Meta:
		ordering = ["-timestamp", "-updated"]

