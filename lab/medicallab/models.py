from django.db import models

class Country(models.Model):
    pass

class Branch(models.Model):
    lab = models.ForeignKey('Lab', related_name='branches')
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='labs', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    is_main = models.NullBooleanField(default=False, blank=True, null=True)

    class Meta:
        unique_together = ("lab", "name")

    @classmethod
    def create_main_branch(cls, lab):
        c = cls()
        c.lab = lab
        c.is_main = True
        c.save()
        
class Lab(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_verified = models.NullBooleanField(default=False, blank=True, null=True)

    class Meta:
        pass

class Job(models.Model):
    branch = models.ForeignKey(Branch, related_name='job_offers')
    closed = models.BooleanField(default=False)
    message = models.CharField(max_length=10000)