from __future__ import unicode_literals

from django.db import models
from doctor.models import Doctor
# Create your models here.


class Patient(models.Model):
    p_user_name = models.CharField(max_length = 35  )#add
    p_first_name = models.CharField(max_length=35)
    p_last_name = models.CharField(max_length=35)
    p_birth_date = models.CharField(max_length=35)
    p_password = models.CharField(max_length = 35)#add
    doc_id = models.ForeignKey(Doctor,default=0);
    #doc = models.ForeignKey(Doctor, default=0)


    def __str__(self):
        return self.p_first_name + ' ' + self.p_last_name
