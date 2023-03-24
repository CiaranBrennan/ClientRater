from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Professor(models.Model):
    code = models.CharField('Professor Code', max_length = 3, unique=True)
    name = models.CharField('Professor Name', max_length = 50)

class Module(models.Model):
    code = models.CharField('Module Code', max_length = 3, unique=True)
    name = models.CharField('Module Name', max_length = 50)

class Instance(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE)
    year = models.IntegerField('Year')
    semester = models.IntegerField('semester')

class Rating(models.Model):
    rating = models.IntegerField("Rating")
    instance = models.ForeignKey(Instance, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
