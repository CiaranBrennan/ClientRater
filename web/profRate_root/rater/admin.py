from django.contrib import admin

# Register your models here.
from .models import Rating, Professor, Instance, Module

admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Instance)
admin.site.register(Rating)
