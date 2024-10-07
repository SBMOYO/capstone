from django.contrib import admin
from .models import House, User, House_image
from django.contrib.admin.models import LogEntry



# Register your models here.
admin.site.register(House)
admin.site.register(User)
admin.site.register(House_image)
