from django.contrib import admin

# Register your models here.
from .models import User, Blog, Comment

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Comment)