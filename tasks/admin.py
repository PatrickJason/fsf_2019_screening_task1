from django.contrib import admin

from .import models
# Register your models here.
from .models import Tasks, Comments


admin.site.register(Tasks)
admin.site.register(Comments)
