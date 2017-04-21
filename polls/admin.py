from django.contrib import admin

# Register your models here.

from .models import Question

admin.site.register(Question) # register Question so that Django knows that it should be displayed on the admin index page