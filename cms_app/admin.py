from django.contrib import admin
# Register your models here.

from .models import *

admin.site.register(Team)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Profile)


