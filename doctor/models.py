from __future__ import unicode_literals
#from patients.models import Patient
from django.db import models

# Create your models here.
#from patients.models import Patient


class Doctor(models.Model):
    d_user_name = models.CharField(max_length = 35 )#add
    d_first_name = models.CharField(max_length = 35)
    d_last_name = models.CharField(max_length = 35)
    d_birth_date = models.CharField(max_length = 35)
    d_password = models.CharField(max_length = 35)#add
    def __unicode__(self):
      return self.d_user_name
    #pats = models.ForeignKey(Patient,  blank=True, null=True, default=0)

    def __str__(self):
        return self.d_first_name + ' ' + self.d_last_name

