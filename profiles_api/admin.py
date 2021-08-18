from django.contrib import admin
from profiles_api import models

#registers our UserProfile model with the admin interface
admin.site.register(models.UserProfile)
