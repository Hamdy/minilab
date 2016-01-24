from django.db import models
from django.contrib.auth import get_user_model

class Attendance(models.Model):
    user = models.ForeignKey(get_user_model())
    attendance = models.DateTimeField('attendance_time')
    departure = models.DateTimeField('departure_time', blank=True, null=True)

    class Meta:
        ordering = ['-attendance']
        
    def __unicode__(self):
        return self.user.username
